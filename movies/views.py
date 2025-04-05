from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from movies.mixins import MovieMixin
from movies.models import Genre, Movie
from users.models import UserMovie
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

class MovieView(MovieMixin, LoginRequiredMixin, ListView):
    """The movies view class."""

    template_name = MovieMixin.mixin_template_name
    model = MovieMixin.mixin_model
    context_object_name = MovieMixin.mixin_context_object_name
    slug = MovieMixin.mixin_slug
    paginate_by = MovieMixin.mixin_paginate_by

    def get_queryset(self):
        self.slug = self.kwargs.get("slug")
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


class UserMovieView(MovieMixin, LoginRequiredMixin, ListView):
    """The user movies view."""

    template_name = MovieMixin.mixin_template_name
    model = MovieMixin.mixin_model
    context_object_name = MovieMixin.mixin_context_object_name
    slug = MovieMixin.mixin_slug
    paginate_by = MovieMixin.mixin_paginate_by

    genres = ""

    def get_queryset(self):
        self.slug = self.kwargs.get("slug")
        movies_users = UserMovie.objects.filter(user=self.request.user).order_by("-id")
        
        if self.slug == "all" or self.slug is None:
            movies = [movie.movie for movie in movies_users]
        else:
            movies = [
                movie.movie
                for movie in movies_users
                if movie.movie.genre.slug == self.slug
            ]

        self.genres = genres = list(set(movie.movie.genre for movie in movies_users))
        self.genres.insert(0, Genre.objects.get(slug="all"))

        return movies

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Фильмы пользователя - Filmora"
        context["heading"] = "Ваша Фильмотека"
        context["text"] = "Здесь расположены фильмы которые вы смотрели."
        context["genres"] = self.genres
        context["selected_genre"] = self.slug
        context["is_user_movies"] = True
        return context


class DetailMovieView(LoginRequiredMixin, DetailView):
    """The concrete movie information view."""

    template_name = "movies/movie.html"
    slug = ""
    model = Movie
    context_object_name = "movie"

    def get_object(self):
        self.slug = self.kwargs.get("slug")
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
