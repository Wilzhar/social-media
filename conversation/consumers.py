# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Conversation, Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("CONNECT===================")
        self.room_name = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        print("DISCONNECT===================")
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("RECEIVE===================")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        chat_id = text_data_json["chat_id"]
        user_id = text_data_json["user_id"]

        # Save message
        await self.save_message(chat_id, user_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "chat_id": chat_id,
                "user_id": user_id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print("CHAT MESSAGE===================")
        message = event["message"]
        chat_id = event["chat_id"]
        user_id = event["user_id"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "chat_id": chat_id,
            "user_id": user_id
        }))

    @database_sync_to_async
    def save_message(self, chat_id, user_id, message):
        conversation = Conversation.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        message = Message(text=message, user=user,
                          conversation=conversation)
        message.save()
