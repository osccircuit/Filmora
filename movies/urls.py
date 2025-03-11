from django.urls import path
from movies import views

app_name = 'movies'

urlpatterns = [
    path('movies/', views.movies, name='films'),
    path('movies/<slug:slug>/', views.movie_details, name='concrete_movie'),
]
