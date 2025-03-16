from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.shortcuts import render

from movies.models import Genre, Movie
from users.models import UserMovie
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
        'title': 'Все Фильмы - Filmora',
        'heading': 'Общая Библиотека Фильмов',
        'text': 'Здесь расположены фильмы которые можно добавить в вашу библиотеку.',
        'movies': current_page,
        'genres': genres,
        'selected_genre': slug,
        'is_user_movies': False,
    }
    return render(request, 'movies/movies.html', context)

@login_required
def user_movies(request, slug='all'):
    """The user movies view."""
    page = request.GET.get('page', 1)
    
    movies_users = UserMovie.objects.filter(user=request.user).order_by('-id')
    genres = list(set(movie.movie.genre for movie in movies_users))
    genres.insert(0, Genre.objects.get(slug='all'))
    
    if slug == 'all':
        movies = [movie.movie for movie in movies_users]
    else:
        movies = [movie.movie for movie in movies_users if movie.movie.genre.slug == slug]
        
    paginator = Paginator(movies, 4)
    current_page = paginator.page(int(page))
    context = {
        'title': 'Фильмы - Filmora',
        'heading': 'Ваша Фильмотека',
        'text': 'Здесь расположены фильмы которые вы смотрели.',
        'movies': current_page,
        'genres': genres,
        'selected_genre': slug,
        'is_user_movies': True,
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
