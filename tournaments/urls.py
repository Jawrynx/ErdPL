from django.urls import path
from. import views

app_name = 'tournament'

urlpatterns = [
    path('tournament/<str:tournament_name>/', views.tournament_view, name='tournament_view'),
    path('tournament/<str:tournament_name>/update_match/<int:match_id>/', views.update_match_view, name='update_match_view'),
]