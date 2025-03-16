from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.shortcuts import render

from movies.models import Genre, Movie
from django.core.paginator import Paginator

@login_required
def movies(request, slug='all'):
    """The movies view."""
    page = request.GET.get('page', 1)
    genres = Genre.objects.all().order_by('-id')
    
    if slug == 'all':
        movies = Movie.objects.all().order_by('-id')
    else:
        movies = Movie.objects.filter(genre__slug=slug).order_by('-id')
        
    paginator = Paginator(movies, 4)
    current_page = paginator.page(int(page))
    context = {
        'title': 'Фильмы - Filmora',
        'heading': 'Библиотека фильмов',
        'text': 'Здесь расположены фильмы которые вы смотрели.',
        'movies': current_page,
        'genres': genres,
        'selected_genre': slug,
    }
    return render(request, 'movies/movies.html', context)

@login_required
def movie_details(request, slug):
    """The concrete movie information view."""
    movie = Movie.objects.filter(slug=slug).first()
    context = {
        'movie': movie,
    }
    return render(request, 'movies/movie.html', context)
