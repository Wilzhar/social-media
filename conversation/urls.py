from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.chats, name="chats"),
    path('chat/<int:chat_id>/', views.chat, name="chat"),
]
