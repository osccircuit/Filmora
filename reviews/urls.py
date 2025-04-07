from django.urls import path
from reviews import views

app_name = 'reviews'

urlpatterns = [
    path('add-review/', views.CreatorReviewView.as_view(), name='add_review'),
    path('delete-review/', views.delete_review, name='delete_review'),
    path('add-mark/', views.add_mark, name='add_mark'),
    path('delete-mark/', views.delete_mark, name='delete_mark')
]
