from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    """Refactor user model"""
    image = models.ImageField(upload_to='users_images',
                              blank=True, null=True,
                              verbose_name='Аватар')
    class Meta():
        """Meta class for User model."""
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return str(self.username).capitalize()

class UserMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_movies')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='movie_users')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name = 'Фильм пользователя'
        verbose_name_plural = 'Фильмы пользователя'

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'