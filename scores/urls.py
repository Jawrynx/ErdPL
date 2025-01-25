from django.urls import path
from . import views


app_name = 'scores'

urlpatterns = [
    path('<str:division_name>/scores/', views.view_scores, name='view_scores'),
    path('<str:division_name>/scores/create/', views.create_score, name='create_score'),
    path('<str:division_name>/scores/<int:match_id>/details/', views.match_details, name='match_details'),
]