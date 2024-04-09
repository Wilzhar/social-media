import factory

from faker import Faker

from ..models import Conversation, Message
from ...authentication.tests.factories import UserFactory

faker = Faker()


class ConversationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Conversation

    user_1 = factory.SubFactory(UserFactory)
    user_2 = factory.SubFactory(UserFactory)
    created_at = factory.LazyAttribute(lambda _: faker.date_time_between())


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    user = factory.SubFactory(UserFactory)
    conversation = factory.SubFactory(ConversationFactory)
    text = factory.LazyAttribute(lambda _: faker.sentence())
