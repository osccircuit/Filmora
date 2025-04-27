from django.urls import path
from movies import views

app_name = 'movies'

urlpatterns = [
    path('', views.MovieView.as_view(), name='films'),
    path('movies/search/', views.MovieView.as_view(), name='movies_search'),
    path('movies/<slug:slug>/', views.MovieView.as_view(), name='films'),
    path('movies/movie/<slug:slug>/', views.DetailMovieView.as_view(), name='concrete_movie'),
    path('user-collection/', views.UserMovieView.as_view(), name='user_movies'),
    path('user-collection/<slug:slug>/', views.UserMovieView.as_view(), name='user_movies'),
]
