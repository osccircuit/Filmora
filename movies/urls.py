from tabnanny import verbose
from django.urls import path
from movies import views

app_name = 'movies'

urlpatterns = [
    path('movies/', views.movies, name='films'),
]
