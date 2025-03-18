from django.shortcuts import redirect, render

def index(request):
    """Main page of the site."""
    if request.user.is_authenticated:
        return redirect('movies:films')
    my_context = {
        'title': 'Главная - Filmora',
        'heading': 'Добро пожаловать в Filmora',
        'text': 'Filmora - это приложение, которое позволяет вам управлять вашей личной библиотекой фильмов. Вы можете добавлять, редактировать и удалять фильмы, а также просматривать информацию о них.',
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
