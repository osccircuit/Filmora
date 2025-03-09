from django.contrib import admin

from movies.models import Movie, Genre


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Movie admin class."""
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Genre admin class."""
    prepopulated_fields = {'slug': ('name',)}
