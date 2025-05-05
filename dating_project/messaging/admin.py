from django.contrib import admin
from .models import Conversation, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0

class ConversationAdmin(admin.ModelAdmin):
    inlines = [MessageInline]

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message)
