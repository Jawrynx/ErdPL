from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/change_password/', views.change_password, name='change_password'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
]
