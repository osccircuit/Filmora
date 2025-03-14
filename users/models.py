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
