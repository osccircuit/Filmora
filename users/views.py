from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm

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
                messages.success(request, f'{username} вы успешно вошли в систему.')
                if request.POST.get('next', None):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect(reverse('movies:films'))
    else:
        form = UserLoginForm()
    
    context = {
        'title': 'Вход - Filmora',
        'form': form,
    }
    return render(request, 'users/login.html', context)

@login_required
def logout(request):
    """Logout page view."""
    messages.success(request, f'{request.user.username} вы успешно вышли из системы.')
    auth.logout(request)
    return redirect(reverse('main:index'))

@login_required
def profile(request):
    """Profile page view."""
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user,
                           files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = ProfileForm(instance=request.user)
        
    context = {
        'title': 'Профиль - Filmora',
        'form': form,
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
            messages.success(request, f'{user.username} вы успешно зарегистрировались.')
            return HttpResponseRedirect(reverse('users:films'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Регистрация - Filmora',
        'form': form,
    }
    return render(request, 'users/registration.html', context)