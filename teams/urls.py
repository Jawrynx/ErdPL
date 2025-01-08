from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('create/', views.create_team, name='create'),
    path('<int:team_id>/join/', views.join_team, name='join'),
    path('<int:team_id>/leave/', views.leave_team, name='leave'),
    path('<int:team_id>/', views.team_detail, name='detail'), 
]