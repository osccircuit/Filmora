from django.contrib import admin

from movies.models import Movie

# admin.site.register(Movie)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}