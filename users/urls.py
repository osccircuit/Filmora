from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('add-to-collection/', views.add_to_collection, name='add_to_collection'),
    path('delete-from-collection/', views.delete_from_collection, name='delete_from_collection'),
]
