from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
   email = forms.CharField(max_length = 100,)
   password = forms.CharField()