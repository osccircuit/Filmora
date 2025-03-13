from django.shortcuts import render

def login(request):
    """Login page view."""
    context = {
        'title': 'Вход - Filmora',
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