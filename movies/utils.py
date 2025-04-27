from django.db.models import Q
from movies.models import Movie

class QSearch:

    def __init__(self, query):
        self.query = query
        self.query_words = None
        self.q_objects = None

    def get_search_queryset(self):
        self.create_query_list(self.query)
        self.create_q_objects()
        return Movie.objects.filter(self.q_objects)
     
    def create_query_list(self, query):
        if not isinstance(query, str):
            self.query_words = None
        self.query_words = [word for word in query.split() if len(word) > 3]

    def create_q_objects(self):
        self.q_objects = Q()
        for token in self.query_words:
           self.q_objects |= Q(title__icontains=token)
           self.q_objects |= Q(description__icontains=token)
        