import json
import re
import requests
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Conversation, Message, Lead
from .services import call_manaja, score_lead
from .sheets import sync_lead

WELCOME = "Bonjour et bienvenue ! 👋 Je suis MANaja, votre conseiller virtuel. Je suis là pour comprendre votre besoin et vous orienter vers la meilleure solution. Qu'est-ce qui vous amène aujourd'hui ?"

@ensure_csrf_cookie
def home(request):
    if not request.session.session_key:
        request.session.create()
    key = request.session.session_key
    convo, created = Conversation.objects.get_or_create(session_key=key)
    source = {k: request.GET.get(k, "")[:300] for k in ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid"] if request.GET.get(k)}
    if source and not convo.profile.get("source"):
        convo.profile["source"] = source
        convo.profile["landing_url"] = request.build_absolute_uri("/")[:500]
        convo.save(update_fields=["profile", "updated_at"])
    if created:
        Message.objects.create(conversation=convo, role="assistant", content=WELCOME)
    history = list(convo.messages.order_by("created_at").values("role", "content"))
    context = {"history_json": json.dumps(history, ensure_ascii=False), "consent_pending": bool(convo.profile.get("consent_requested") and convo.status != "submitted"), "submitted": convo.status == "submitted"}
    return render(request, "landing.html", context)

def _rate_limited(request):
    ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "unknown")).split(",")[0].strip()
    key = "chat-rate:" + ip
    count = cache.get(key, 0)
    if count >= settings.RATE_LIMIT_CHAT_PER_MINUTE:
        return True
    cache.set(key, count + 1, 60)
    return False

@require_POST
def reset(request):
    if request.session.session_key:
        Conversation.objects.filter(session_key=request.session.session_key, status__in=["in_progress", "consent_pending"]).delete()
    request.session.flush()
    request.session.create()
    return JsonResponse({"ok": True})

@require_GET
def status(request):
    return JsonResponse({"ok": True, "ai_configured": bool(settings.MANAJA_API_BASE_URL and settings.MANAJA_MODEL)})

@require_POST
def chat(request):
    if _rate_limited(request):
        return JsonResponse({"error": "Trop de messages en peu de temps. Réessayez dans une minute."}, status=429)
    try:
        data = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Requête JSON invalide."}, status=400)
    text = re.sub(r"<[^>]*>", "", str(data.get("message", ""))).strip()
    if not text or len(text) > 4000:
        return JsonResponse({"error": "Votre message doit contenir entre 1 et 4 000 caractères."}, status=400)
    if not request.session.session_key:
        request.session.create()
    convo, _ = Conversation.objects.get_or_create(session_key=request.session.session_key)
    if convo.status == "submitted":
        return JsonResponse({"error": "Cette demande a déjà été transmise. Vous pouvez démarrer une nouvelle conversation en rechargeant la page."}, status=409)
    if convo.profile.get("consent_requested") and text.lower() in {"oui", "yes", "eny", "e", "ok", "d'accord", "daccord"}:
        return JsonResponse({"error": "Pour protéger vos données, confirmez avec le bouton de consentement affiché sous le récapitulatif."}, status=400)
    recent = list(convo.messages.order_by("-created_at")[:16])
    recent.reverse()
    history = [{"role": m.role, "content": m.content} for m in recent]
    history.append({"role": "user", "content": text})
    try:
        result = call_manaja(history)
    except requests.Timeout:
        return JsonResponse({"error": "Le conseiller met trop de temps à répondre. Réessayez."}, status=504)
    except requests.RequestException:
        return JsonResponse({"error": "Le service IA est temporairement indisponible. Réessayez plus tard."}, status=502)
    except (RuntimeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        return JsonResponse({"error": str(exc) if settings.DEBUG else "Le service IA n'est pas configuré ou a renvoyé une réponse invalide."}, status=503)
    with transaction.atomic():
        Message.objects.create(conversation=convo, role="user", content=text)
        Message.objects.create(conversation=convo, role="assistant", content=result["reply"])
        profile = dict(convo.profile)
        profile.update({k: v for k, v in result["profile_patch"].items() if v is not None and v != ""})
        if result["profile_patch"].get("language"):
            convo.language = str(result["profile_patch"]["language"])[:12]
        convo.profile = profile
        convo.save(update_fields=["profile", "language", "updated_at"])
    return JsonResponse({"reply": result["reply"], "consent_requested": bool(profile.get("consent_requested")), "progress": _progress(profile), "qualified": result["qualified"]})

def _progress(profile):
    keys = ["need", "service", "problem", "goal"]
    known = sum(bool(profile.get(k)) for k in keys)
    return min(100, known * 20 + (20 if profile.get("name") or profile.get("email") else 0))

@require_POST
def consent(request):
    try:
        payload = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Requête invalide."}, status=400)
    if payload.get("consent") is not True:
        return JsonResponse({"error": "Le consentement explicite est requis."}, status=400)
    key = request.session.session_key
    if not key:
        return JsonResponse({"error": "Conversation introuvable."}, status=404)
    convo = Conversation.objects.filter(session_key=key).first()
    if not convo or not convo.profile.get("consent_requested"):
        return JsonResponse({"error": "L'assistant n'a pas encore demandé votre autorisation. Continuez la conversation."}, status=400)
    with transaction.atomic():
        convo.consent_at = timezone.now()
        convo.status = "submitted"
        convo.profile["consent_granted"] = True
        convo.save(update_fields=["consent_at", "status", "profile", "updated_at"])
        score, temperature = score_lead(convo.profile)
        lead, _ = Lead.objects.get_or_create(conversation=convo, defaults={"data": {k: v for k, v in convo.profile.items() if k not in {"source", "landing_url", "consent_requested", "consent_granted"}}, "score": score, "temperature": temperature, "status": "qualified" if score >= 50 else "new", "source": convo.profile.get("source", {})})
    sheets_state = "not_configured"
    if settings.GOOGLE_SHEETS_ENABLED:
        try:
            sync_lead(lead)
            sheets_state = "synced"
        except Exception as exc:
            lead.sheets_error = str(exc)[:1000]
            lead.save(update_fields=["sheets_error"])
            sheets_state = "pending_retry"
    if settings.LEAD_NOTIFICATION_WEBHOOK:
        try:
            requests.post(settings.LEAD_NOTIFICATION_WEBHOOK, json={"lead_id": str(lead.id), "score": lead.score, "temperature": lead.temperature}, timeout=4).raise_for_status()
        except requests.RequestException:
            pass
    Message.objects.create(conversation=convo, role="assistant", content="Merci pour votre confiance ! Votre demande a bien été transmise à notre équipe. Nous reviendrons vers vous selon le moyen de contact convenu.")
    return JsonResponse({"ok": True, "lead_id": str(lead.id), "score": lead.score, "temperature": lead.temperature, "sheets": sheets_state, "message": "Merci pour votre confiance ! Votre demande a bien été transmise à notre équipe. Nous reviendrons vers vous selon le moyen de contact convenu."})
