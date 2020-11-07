from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate

from user_auth.models import User


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")
