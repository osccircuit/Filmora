from movies.models import Movie


class MovieMixin:
    """Mixin for movie view classes"""
    mixin_template_name = "movies/movies.html"
    mixin_model = Movie
    mixin_context_object_name = "movies"
    mixin_slug = "all"
    mixin_paginate_by = 4
