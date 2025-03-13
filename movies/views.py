from django.core import paginator
from django.shortcuts import render

from movies.models import Genre, Movie
from django.core.paginator import Paginator

def movies(request):
    """The movies view."""
    
    page = request.GET.get('page', 1)
    
    movies = Movie.objects.all()
    genres = Genre.objects.all().order_by('-id')
    
    paginator = Paginator(movies, 4)
    current_page = paginator.page(int(page))
    context = {
        'title': 'Фильмы - Filmora',
        'heading': 'Библиотека фильмов',
        'text': 'Здесь расположены фильмы которые вы смотрели.',
        'movies': current_page,
        'genres': genres,
    }
    return render(request, 'movies/movies.html', context)


def movie_details(request, slug):
    """The concrete movie information view."""
    movie = Movie.objects.filter(slug=slug).first()
    context = {
        'movie': movie,
    }
    return render(request, 'movies/movie.html', context)
