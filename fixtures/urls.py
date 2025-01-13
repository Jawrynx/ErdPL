from django.urls import path
from . import views

app_name = 'fixtures'

urlpatterns = [
    path('<int:division_number>/fixtures/', views.fixtures_by_division, name='fixtures_by_division'), 
]