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
    reviews = UserMovie.objects.filter(movie__id=movie.id, user=request.user) \
    .values('review')
    
    all_reviews = UserMovie.objects.filter(movie__id=movie.id) \
    .select_related('user') \
    .values_list('user__username', 'user__image', 'added_at', 'review', 'mark') \
    .all()
    
    if reviews.count() == 0:
        review_not_add = 'not_add'
    elif not reviews[0].get('review'):
        review_not_add = 'empty'
    else:
        review_not_add = 'full'
    
    if UserMovie.objects.filter(user=request.user, movie=movie).first() is None:
        user_movie = None
    else:
        user_movie = True
        
    n_reviews = UserMovie.objects.filter(movie__id=movie.id).select_related('user')
        
    context = {
        'movie': movie,
        'user_movie': user_movie,
        'reviews': n_reviews,
        'review_not_add': review_not_add,
    }
    return render(request, 'movies/movie.html', context)
