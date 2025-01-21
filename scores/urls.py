from django.urls import path
from . import views


app_name = 'scores'

urlpatterns = [
    path('<str:division_name>/scores/', views.view_scores, name='view_scores'),
]