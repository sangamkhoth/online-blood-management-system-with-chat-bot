from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'sentiment')
    search_fields = ('message', 'response', 'user__username')
    list_filter = ('sentiment', 'created_at')
