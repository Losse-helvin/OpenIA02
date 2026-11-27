import json
import requests
from django.conf import settings

SYSTEM_PROMPT = """Tu es MANaja, un conseiller commercial chaleureux, honnête et professionnel. Tu réponds dans la langue du visiteur (français, malgache ou anglais) et tu peux gérer les fautes et formulations courtes. Comprends d'abord librement le besoin, puis pose UNE seule question utile à la fois. N'ouvre jamais par nom/téléphone. Évite répétitions; n'invente aucune donnée, aucun tarif ni promesse. Fais une première reformulation utile avant de demander les coordonnées. Les coordonnées sont facultatives sauf contact demandé par le visiteur. Explique leur finalité et demande un consentement explicite avant tout enregistrement ou suivi commercial. Résume les informations et demande confirmation. Ne prétends pas qu'un enregistrement a eu lieu avant consentement.

Tu dois renvoyer exclusivement un JSON valide avec les clés: reply (string), profile_patch (object des champs réellement fournis; champs autorisés: name,email,phone,company,job_title,country,city,address,language,service,need,problem,goal,budget,timeline,urgency,contact_channel,objections,intent,consent_requested), qualified (boolean). Si un champ est inconnu, ne le renvoie pas ou utilise null; ne déduis pas budget/intention. consent_requested doit être true uniquement si tu as déjà compris le besoin, fourni une première valeur et tu demandes clairement l'autorisation de transmettre les infos à l'équipe. Ne déclenche jamais un consentement en inférant un oui. Un clic distinct du visiteur sera traité par le backend."""

ALLOWED_PROFILE_FIELDS = {"name", "email", "phone", "company", "job_title", "country", "city", "address", "language", "service", "need", "problem", "goal", "budget", "timeline", "urgency", "contact_channel", "objections", "intent", "consent_requested"}

def call_manaja(messages):
    if not settings.MANAJA_API_BASE_URL or not settings.MANAJA_MODEL:
        raise RuntimeError("MANaja AI n'est pas configuré. Renseignez MANAJA_API_BASE_URL, MANAJA_API_KEY et MANAJA_MODEL dans .env.")
    url = settings.MANAJA_API_BASE_URL + "/chat/completions"
    headers = {"Content-Type": "application/json"}
    if settings.MANAJA_API_KEY:
        headers["Authorization"] = "Bearer " + settings.MANAJA_API_KEY
    payload = {"model": settings.MANAJA_MODEL, "temperature": 0.55, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *messages]}
    response = requests.post(url, headers=headers, json=payload, timeout=settings.MANAJA_TIMEOUT_SECONDS)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    if not isinstance(parsed.get("reply"), str):
        raise ValueError("Réponse MANaja inattendue")
    patch = parsed.get("profile_patch", {})
    if not isinstance(patch, dict):
        patch = {}
    return {"reply": parsed["reply"], "profile_patch": {k: v for k, v in patch.items() if k in ALLOWED_PROFILE_FIELDS and isinstance(v, (str, int, float, bool, list, type(None)))}, "qualified": bool(parsed.get("qualified", False))}

def score_lead(profile):
    # Points conservateurs: aucune valeur inconnue ne reçoit de points.
    relevance = 25 if profile.get("service") else (12 if profile.get("need") else 0)
    clarity = 20 if profile.get("problem") and profile.get("goal") else (12 if profile.get("need") or profile.get("problem") else 0)
    urgency = 15 if str(profile.get("urgency", "")).lower() in {"urgent", "immédiat", "immediate", "cette semaine", "asap"} else (7 if profile.get("timeline") else 0)
    budget = 20 if profile.get("budget") else 0
    intent = 20 if str(profile.get("intent", "")).lower() in {"high", "forte", "prêt", "ready", "buying", "achat", "devis"} else (10 if profile.get("contact_channel") or profile.get("timeline") else 0)
    total = min(100, relevance + clarity + urgency + budget + intent)
    return total, "hot" if total >= 80 else "warm" if total >= 50 else "cold"
