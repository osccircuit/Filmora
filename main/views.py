from django.shortcuts import render

def index(request):
    """Main page of the site."""
    my_context = {
        'title': 'Главная - Filmora',
        'heading': 'Добро пожаловать на главную страницу!',
        'text': 'Здесь вы можете найти много интересного и полезного.'
    }
    return render(request, 'main/index.html', my_context)

def about(request):
    """About page of the site."""
    my_context = {
        'title': 'О нас - Filmora',
        'heading': 'О нас',
        'text': 'Это страница "О нас" данного сайта.'
    }
    return render(request, 'main/about.html', my_context)
