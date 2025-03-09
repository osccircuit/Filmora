from django.shortcuts import render

from movies.models import Genre, Movie

def movies(request):
    """The movies view."""
    movies = Movie.objects.all()
    genres = Genre.objects.all().order_by('-id')
    context = {
        'title': 'Фильмы - Filmora',
        'heading': 'Библиотека фильмов',
        'text': 'Здесь расположены фильмы которые вы смотрели.',
        'movies': movies,
        'genres': genres
    }
    return render(request, 'movies/movies.html', context)
