from contextvars import copy_context
from urllib import response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth, messages
from django.core import paginator
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from movies.models import Movie
import reviews
from users.models import UserMovie
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
import copy


class UserLoginView(LoginView):
    """Login page view."""

    template_name = "users/login.html"
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("user:logout"):
            return redirect_page
        return reverse_lazy("movies:films")

    def form_valid(self, form):
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            messages.success(
                self.request, f"{user.username} вы успешно вошли в систему."
            )
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход - Filmora"
        return context


class LogoutView(LoginRequiredMixin, View):
    """Profile page view."""

    def get(self, request, *args, **kwargs):
        messages.success(
            request, f"{request.user.username} вы успешно вышли " "из системы."
        )
        auth.logout(request)
        return HttpResponseRedirect(reverse("main:index"))
    
class ProfileView(LoginRequiredMixin, UpdateView):
    """Profile page view."""

    template_name = "users/profile.html"
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Профиль - Filmora"
        return context


class RegistrationView(CreateView):
    """Registration page view."""

    template_name = "users/registration.html"
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse_lazy("movies:films")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация - Filmora"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        user = form.instance

        if user:
            auth.login(self.request, user)

        messages.success(
            self.request, f"{user.username} вы успешно зарегистрировались."
        )
        return HttpResponseRedirect(self.get_success_url())


class ButtonCollectionView(View):
    """Handle add movie in collection methods"""

    def post(self, request):
        """Get ajax data from frontend and handling add movie to collection"""
        movie_id = self.request.POST.get('movie_id')
        if movie_id is None:
            return JsonResponse({"error": "Не передан ID фильма."}, status=400)

        movie = Movie.objects.get(id=movie_id)
        UserMovie.objects.create(user=request.user, movie=movie, review=None)

        button_add = render_to_string(
            "includes/add_to_collect_btn.html",
            {"movie": movie, "user_movie": True},
            request,
        )

        review_form = render_to_string(
            "includes/add_review.html", 
            {"review_not_add": True, "movie": movie, 'user_movie': True},
            request
        )

        response_data = {
            "message": "Фильм успешно добавлен в вашу коллекцию.",
            "button_add": button_add,
            "review_form": review_form,
        }
        return JsonResponse(response_data)

class ButtonDeleteView(View):
    """Handle delete movie from collection methods"""
    paginator = None
    current_page = 1
    paginate_by = 3
        
    def post(self, request):
        """Delete movie from collection POST"""

        movie_id = request.POST.get("movie_id")

        if movie_id is None:
            return JsonResponse({"error": "Не передан ID фильма."}, status=400)

        all_user_movie_info = UserMovie.objects.filter(movie__id=movie_id).select_related('movie')
        this_user_movie = all_user_movie_info.filter(user=request.user).get(movie__id=movie_id)
        original_movie = all_user_movie_info.filter(user=request.user).first().movie
        this_user_movie.delete()

        self.paginator = Paginator(all_user_movie_info.exclude(user=request.user), self.paginate_by)

        button_delete = render_to_string(
            "includes/add_to_collect_btn.html",
            {"movie": original_movie, "user_movie": False},
            request,
        )

        review_form = render_to_string(
            "includes/add_review.html",
            {"review_not_add": False, 'user_movie': False, "movie": original_movie},
            request,
        )

        users_reviews = render_to_string(
            "includes/view_reviews.html", {"reviews": self.paginator.page(self.current_page)},
            request
        )

        response_data = {
            "message": "Фильм успешно удален из вашей коллекции.",
            "button_add": button_delete,
            "review_form": review_form,
            "users_reviews": users_reviews,
        }
        return JsonResponse(response_data)