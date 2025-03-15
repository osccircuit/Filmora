from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm

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
    auth.logout(request)
    return redirect(reverse('main:index'))

def profile(request):
    """Profile page view."""
    context = {
        'title': 'Профиль - Filmora',
    }
    return render(request, 'users/profile.html', context)

def registration(request):
    """Registration page view."""
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Регистрация - Filmora',
        'form': form,
    }
    return render(request, 'users/registration.html', context)