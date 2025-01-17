from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('create/', views.create_team, name='create'),
    path('<int:team_id>/join/', views.join_team, name='join'),
    path('<str:team_name>/leave/', views.leave_team, name='leave'),
    path('<str:team_name>/profile/', views.team_detail, name='detail'),
    path('<str:team_name>/edit/', views.edit_team, name='edit_team'),
    path('<str:team_name>/edit_members/', views.edit_team_members, name='edit_team_members'),
    path('<str:team_name>/delete/', views.delete_team, name='delete_team'),
    path('<str:team_name>/remove_member/<int:member_id>/', views.remove_team_member, name='remove_team_member'),
]