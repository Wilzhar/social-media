from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Conversation(models.Model):
    user_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_1"
    )

    user_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_2"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    text = models.CharField(max_length=100, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
