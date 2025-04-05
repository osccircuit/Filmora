from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView, ListView
from movies.models import Genre, Movie
from users.models import UserMovie
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class MovieView(LoginRequiredMixin, ListView):
    """The movies view class."""

    template_name = "movies/movies.html"
    model = Movie
    context_object_name = "movies"
    slug = "all"
    paginate_by = 4

    def get_queryset(self):
        self.slug = self.kwargs.get('slug')
        if self.slug == "all" or self.slug is None:
            # pylint: disable=no-member
            movies = Movie.objects.all().order_by("-id")  # type: ignore
        else:
            # pylint: disable=no-member
            movies = Movie.objects.filter(genre__slug=self.slug)  # type: ignore
        return movies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Все Фильмы - Filmora"
        context["heading"] = "Общая Библиотека Фильмов"
        context["text"] = (
            "Здесь расположены фильмы которые можно добавить " "в вашу библиотеку."
        )
        # pylint: disable=no-member
        context["genres"] = Genre.objects.all().order_by("-id")
        context["selected_genre"] = self.slug
        context["is_user_movies"] = False
        return context


# @login_required
# def movies(request, slug='all'):
#     """The movies view."""
#     page = request.GET.get('page', 1)
#     genres = Genre.objects.all().order_by('-id')

#     if slug == 'all':
#         movies = Movie.objects.all().order_by('-id')
#     else:
#         movies = Movie.objects.filter(genre__slug=slug).order_by('-id')

#     paginator = Paginator(movies, 4)
#     current_page = paginator.page(int(page))
#     context = {
#         'title': 'Все Фильмы - Filmora',
#         'heading': 'Общая Библиотека Фильмов',
#         'text': 'Здесь расположены фильмы которые можно добавить в вашу библиотеку.',
#         'movies': current_page,
#         'genres': genres,
#         'selected_genre': slug,
#         'is_user_movies': False,
#     }
#     return render(request, 'movies/movies.html', context)


@login_required
def user_movies(request, slug="all"):
    """The user movies view."""
    page = request.GET.get("page", 1)

    movies_users = UserMovie.objects.filter(user=request.user).order_by("-id")
    genres = list(set(movie.movie.genre for movie in movies_users))
    genres.insert(0, Genre.objects.get(slug="all"))

    if slug == "all":
        movies = [movie.movie for movie in movies_users]
    else:
        movies = [
            movie.movie for movie in movies_users if movie.movie.genre.slug == slug
        ]

    paginator = Paginator(movies, 4)
    current_page = paginator.page(int(page))
    context = {
        "title": "Фильмы - Filmora",
        "heading": "Ваша Фильмотека",
        "text": "Здесь расположены фильмы которые вы смотрели.",
        "movies": current_page,
        "genres": genres,
        "selected_genre": slug,
        "is_user_movies": True,
    }
    return render(request, "movies/movies.html", context)


class DetailMovieView(LoginRequiredMixin, DetailView):
    """The concrete movie information view."""

    template_name = 'movies/movie.html'
    slug = ''
    model = Movie
    context_object_name = 'movie'

    def get_object(self):
        self.slug = self.kwargs.get('slug')
        if self.slug is None or self.slug == "":
            return 0
        movie = Movie.objects.filter(slug=self.slug).first()
        return movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get("page", 1)

        all_reviews = UserMovie.objects.filter(movie__slug=self.slug)

        cur_user_data = all_reviews.filter(user=self.request.user).first()
        cur_user_review = cur_user_data.review if cur_user_data else None
        cur_user_movie = cur_user_data.movie if cur_user_data else None

        paginator = Paginator(all_reviews, 3)
        try:
            current_page = paginator.page(int(page))
        except (PageNotAnInteger, EmptyPage):
            current_page = paginator.page(1)

        context["user_movie"] = bool(cur_user_movie)
        context["reviews"] = current_page
        context["review_not_add"] = not bool(cur_user_review)
        return context