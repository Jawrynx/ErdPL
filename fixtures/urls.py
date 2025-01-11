from django.urls import path
from . import views

app_name = 'fixtures'

urlpatterns = [
    path('division1/', views.fixtures_home, name='fixtures_home'),
]