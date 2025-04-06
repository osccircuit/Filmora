from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add-to-collection/', views.ButtonCollectionView.as_view(), name='add_to_collection'),
    path('delete-from-collection/', views.delete_from_collection, name='delete_from_collection'),
]
