from django.urls import path
from . import views

app_name = 'fixtures'

urlpatterns = [
    path('<str:division_name>/fixtures/', views.fixtures_by_division, name='fixtures_by_division'), 
]