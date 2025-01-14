from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('create/', views.create_team, name='create'),
    path('<int:team_id>/join/', views.join_team, name='join'),
    path('<int:team_id>/leave/', views.leave_team, name='leave'),
    path('<int:team_id>/', views.team_detail, name='detail'), 
    path('<int:team_id>/edit/', views.edit_team, name='edit_team'),
    path('<int:team_id>/edit_members/', views.edit_team_members, name='edit_team_members'),
    path('<int:team_id>/delete/', views.delete_team, name='delete_team'),
    path('<int:team_id>/remove_member/<int:member_id>/', views.remove_team_member, name='remove_team_member'),
]