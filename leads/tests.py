import json
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from .models import Conversation, Lead
from .services import score_lead

class ScoringTests(TestCase):
    def test_empty_profile_has_no_points(self):
        self.assertEqual(score_lead({}), (0, "cold"))
    def test_complete_urgent_profile_scores_hot(self):
        score, category = score_lead({"service":"site web", "need":"refonte", "problem":"peu de contacts", "goal":"plus de clients", "urgency":"urgent", "budget":"1000 EUR", "intent":"ready"})
        self.assertEqual((score, category), (100, "hot"))
    def test_unknown_budget_is_not_scored(self):
        score, _ = score_lead({"service":"site web", "need":"creation", "problem":"pas de site", "goal":"vendre"})
        self.assertEqual(score, 45)

class ConversationTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.client.get("/")

    @patch("leads.views.call_manaja")
    def test_chat_saves_messages_and_profile(self, ai):
        ai.return_value = {"reply":"Vous voulez un site existant ou nouveau ?", "profile_patch":{"need":"développer un site", "service":"site web"}, "qualified":False}
        response = self.client.post("/api/chat", data=json.dumps({"message":"Je veux développer un site"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        conversation = Conversation.objects.get()
        self.assertEqual(conversation.messages.count(), 3)
        self.assertEqual(conversation.profile["service"], "site web")

    def test_lead_not_saved_without_explicit_consent(self):
        response = self.client.post("/api/consent", data=json.dumps({"consent":True}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Lead.objects.count(), 0)

    @patch("leads.views.call_manaja")
    def test_consent_creates_lead_only_after_offer(self, ai):
        ai.return_value = {"reply":"J'ai bien compris. Puis-je transmettre votre projet à l'équipe ?", "profile_patch":{"need":"un site", "service":"site web", "consent_requested":True}, "qualified":True}
        self.client.post("/api/chat", data=json.dumps({"message":"Je veux un site web"}), content_type="application/json")
        response = self.client.post("/api/consent", data=json.dumps({"consent":True}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertTrue(Conversation.objects.get().consent_at)
        self.assertEqual(response.json()["sheets"], "not_configured")
