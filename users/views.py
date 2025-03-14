from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserLoginForm

def login(request):
    """Login page view."""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,
                                                          password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    
    context = {
        'title': 'Вход - Filmora',
        'form': form,
    }
    return render(request, 'users/login.html', context)

def logout(request):
    """Logout page view."""
    context = {
        'title': 'Выход - Filmora',
    }
    return render(request, '', context)

def profile(request):
    """Profile page view."""
    context = {
        'title': 'Профиль - Filmora',
    }
    return render(request, 'users/profile.html', context)

def registration(request):
    """Registration page view."""
    context = {
        'title': 'Регистрация - Filmora',
    }
    return render(request, 'users/registration.html', context)