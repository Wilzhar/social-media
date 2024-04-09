from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm

# - Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate


# Create your views here.


def home(request):
    return render(request, "home.html")


def login(request):

    if request.user.is_authenticated:
        return redirect("conversation/chats")

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("conversation/chats")

    context = {'loginform': form}

    return render(request, "authentication/login.html", context)


def register(request):

    if request.user.is_authenticated:
        return redirect("conversation/chats")

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("login")

    context = {'registerform': form}

    return render(request, 'authentication/register.html', context=context)


def user_logout(request):
    auth.logout(request)
    return redirect("/")
