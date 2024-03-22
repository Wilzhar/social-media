from django import forms
from django.forms.widgets import TextInput


class MessageForm(forms.Form):
    text = forms.CharField(widget=TextInput())
