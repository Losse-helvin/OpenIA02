import uuid
from django.db import models

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_key = models.CharField(max_length=64, unique=True, db_index=True)
    language = models.CharField(max_length=12, default="fr")
    profile = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default="in_progress")
    consent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=12, choices=[("user", "User"), ("assistant", "Assistant")])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.OneToOneField(Conversation, on_delete=models.PROTECT, related_name="lead")
    data = models.JSONField(default=dict)
    score = models.PositiveSmallIntegerField(default=0)
    temperature = models.CharField(max_length=12, default="cold")
    status = models.CharField(max_length=24, default="qualified")
    source = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sheets_synced_at = models.DateTimeField(null=True, blank=True)
    sheets_error = models.TextField(blank=True)
