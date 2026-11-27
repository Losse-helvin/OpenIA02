from django.contrib import admin
from .models import Conversation, Message, Lead

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("role", "content", "created_at")
    can_delete = False

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "language", "created_at", "updated_at")
    readonly_fields = ("id", "session_key", "created_at", "updated_at", "consent_at")
    inlines = [MessageInline]

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("id", "score", "temperature", "status", "created_at", "sheets_synced_at")
    readonly_fields = ("id", "created_at", "sheets_synced_at", "sheets_error")
