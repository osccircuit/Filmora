from django.urls import path
from movies import views

app_name = 'movies'

urlpatterns = [
    path('', views.movies, name='films'),
    path('<slug:slug>/', views.movies, name='films'),
    path('movies/<slug:slug>/', views.movie_details, name='concrete_movie'),
]
