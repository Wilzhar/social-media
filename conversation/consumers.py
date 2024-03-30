# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Conversation, Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        chat_id = text_data_json["chat_id"]
        user_id = text_data_json["user_id"]

        # Save message
        await self.save_message(chat_id, user_id, message)

        message_model = await self.get_message(chat_id)

        # Format date: March 30, 2024, 10:26 a.m.
        created_at = message_model.created_at.strftime("%B %d, %Y, %I:%M %p")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "chat_id": chat_id,
                "user_id": user_id,
                "created_at": created_at,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        chat_id = event["chat_id"]
        user_id = event["user_id"]
        created_at = event["created_at"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "chat_id": chat_id,
            "user_id": user_id,
            "created_at": created_at,
        }))

    @database_sync_to_async
    def save_message(self, chat_id, user_id, message):
        conversation = Conversation.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        message = Message(text=message, user=user,
                          conversation=conversation)
        message.save()

    @database_sync_to_async
    def get_message(self, chat_id):
        return Message.objects.filter(conversation_id=chat_id).order_by('-created_at').first()
