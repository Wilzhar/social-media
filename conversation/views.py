from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Conversation, Message


@login_required(login_url="login")
def chat(request, user_1_id, user_2_id):
    chat = Conversation.objects.filter(
        user_1=user_1_id, user_2=user_2_id).first()

    if not chat:
        chat = Conversation.objects.filter(
            user_1=user_2_id, user_2=user_1_id).first()

        if not chat:
            user_1 = User.objects.get(id=user_1_id)
            user_2 = User.objects.get(id=user_2_id)
            chat = Conversation(user_1=user_1, user_2=user_2)
            chat.save()

    messages = Message.objects.filter(
        conversation_id=chat.id).order_by('-created_at')[:10]

    context = {'chat': chat, 'messages': messages,
               'chat_id': chat.id}

    return render(request, "chats/chat.html", context)


@login_required(login_url="login")
def chats(request):
    current_user = request.user

    chats_user_1 = Conversation.objects.filter(user_1_id=current_user.id)
    chats_user_2 = Conversation.objects.filter(user_2_id=current_user.id)

    all_chats = chats_user_1 | chats_user_2

    return render(request, "chats/chats.html", {'chats': all_chats})


def users(request):
    users = User.objects.all
    return render(request, "chats/users.html", {"users": users})


def load_messages(request):
    chat_id = request.GET.get('chat_id')
    offset = int(request.GET.get('offset'))
    messages = Message.objects.filter(conversation_id=chat_id).order_by(
        '-created_at')[offset:offset+10]
    messages_list = []
    for message in messages:
        created_at = message.created_at.strftime("%B %d, %Y, %H:%M %p")
        message_list = {
            'created_at': created_at,
            'text': message.text,
            'user_id': message.user.id
        }
        messages_list.append(message_list)
    data = {
        'messages': messages_list
    }
    return JsonResponse(data=data)
