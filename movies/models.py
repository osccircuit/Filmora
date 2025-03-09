from django.db import models


class Genre(models.Model):
    """The Genre model."""
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=200, blank=True,
                            null=True, verbose_name='URL')
    
    class Meta():
        """Meta class for Genre model."""
        db_table = 'genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Movie(models.Model):
    """The Movie model."""
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=200, blank=True,
                            null=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    year = models.IntegerField(blank=True, null=True, verbose_name='Год')
    country = models.CharField(max_length=200, blank=True, verbose_name='Страна')
    genre = models.CharField(max_length=200, blank=True, verbose_name='Жанр')
    image = models.ImageField(upload_to='movies', blank=True, null=True, verbose_name='Постер')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')

    class Meta():
        """Meta class for Movie model."""
        db_table = 'movie'
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'