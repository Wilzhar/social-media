from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Conversation, Message
from .forms import MessageForm

# Create your views here.


@login_required(login_url="login")
def chat(request, chat_id):
    chat = Conversation.objects.filter(id=chat_id).first()

    messages = Message.objects.filter(
        conversation_id=chat_id).order_by('created_at')

    # form = MessageForm()

    # if request.method == 'POST':
    #     data = request.POST
    #     form = MessageForm(request.POST)

    #     if form.is_valid():
    #         text = request.POST.get('text')

    #         conversation = Conversation.objects.get(id=chat_id)
    #         message = Message(text=text, user=request.user,
    #                           conversation=conversation)
    #         message.save()
    #         return HttpResponseRedirect('')

    context = {'chat': chat, 'messages': messages,
               'chat_id': chat_id}  # 'messageform': form

    return render(request, "chat.html", context)


@login_required(login_url="login")
def chats(request):
    current_user = request.user

    chats_user_1 = Conversation.objects.filter(user_1_id=current_user.id)
    chats_user_2 = Conversation.objects.filter(user_2_id=current_user.id)

    all_chats = chats_user_1 | chats_user_2

    return render(request, "chats.html", {'chats': all_chats})