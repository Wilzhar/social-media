from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.chats, name="chats"),
    path('chat/<int:user_1_id>/<int:user_2_id>', views.chat, name="chat"),
    path('users/', views.users, name="users"),
]
