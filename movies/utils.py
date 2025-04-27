from django.db.models import Value
from movies.models import Movie
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


class QSearch:

    def __init__(self, query):
        self.vector = SearchVector("title", "description")
        self.query = SearchQuery(query)
        self.rank = SearchRank(self.vector, self.query)

    def get_search_queryset(self):
        result = (
            Movie.objects.annotate(rank=self.rank)
            .filter(rank__gt=0.0002)
            .order_by("-rank")
        )

        return result
