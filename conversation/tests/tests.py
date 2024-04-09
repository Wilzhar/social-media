from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from ...authentication.tests import UserFactory
from django.urls import reverse
from factories import ConversationFactory, MessageFactory

from ..models import Conversation, Message


class ConversationTestCase(TestCase):
    def test_conversation_creation(self):
        client = Client()

        user_1 = UserFactory()
        user_2 = UserFactory()

        conversation = ConversationFactory(
            user_1_id=user_1.id, user_2_id=user_2.id)

        MessageFactory.create_batch(
            5, user_id=user_1.id, conversation_id=conversation.id)
        MessageFactory.create_batch(
            5, user_id=user_2.id, conversation_id=conversation.id)

        response = client.post(
            reverse('chat'), {'user_1_id': user_1.id, 'user_2_id': user_2.id})

        self.assertEqual(response.status_code, 200)

        client.logout()
