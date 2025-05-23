import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    """User login form."""
    username = forms.CharField()
    password = forms.CharField()
    
    class Meta:
        """Meta class for user login form."""
        model = User
        fields = ['username', 'password']
class UserRegistrationForm(UserCreationForm):
    """Class for user registration form."""
    class Meta:
        """Meta class for user registration form."""
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
        
class ProfileForm(UserChangeForm):
    """Class for user profile form."""
    class Meta:
        """Meta class for user profile form."""
        model = User
        fields = (
            'username',
            'email',
            'image',
        )
        
    image= forms.ImageField(required=False)
    username = forms.CharField()
    email = forms.CharField()