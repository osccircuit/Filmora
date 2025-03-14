from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={"autofocus": True,
                                                             "id": 'username'}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                          'id': 'password'}),
    )
    
    class Meta:
        model = User
        fields = ['username', 'password']