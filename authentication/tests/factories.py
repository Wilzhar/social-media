import factory

from django.contrib.auth.models import User
from faker import Faker

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    password = factory.PostGenerationMethodCall('set_password', 'password')
