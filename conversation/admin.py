from django.contrib import admin
from .models import Conversation, Message


class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]


# Register your models here.
admin.site.register(Conversation)
admin.site.register(Message, MessageAdmin)
