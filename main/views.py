from django.shortcuts import redirect, render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('movies:films')
        return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная - Filmora'
        context['heading'] = 'Добро пожаловать в Filmora'
        context['text'] = 'Filmora - это приложение, которое позволяет вам управлять вашей личной библиотекой фильмов. Вы можете добавлять, редактировать и удалять фильмы, а также просматривать информацию о них.'
        return context


def about(request):
    """About page of the site."""
    my_context = {
        'title': 'О нас - Filmora',
        'heading': 'О нас',
        'text': 'Это страница "О нас" данного сайта.'
    }
    return render(request, 'main/about.html', my_context)
