from django.db import models
from django.contrib.auth import get_user_model
from users.models import Player
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

User = get_user_model()

class Division(models.Model):
    name = models.CharField(max_length=255, unique=True)
    start_date = models.DateField(default=timezone.now)
    num_weeks = models.IntegerField(default=22) 

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name='captain_of')
    members = models.ManyToManyField(Player, related_name='teams')
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True) 
    team_image = models.ImageField(upload_to='team_images/', storage=FileSystemStorage(), blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
    
    def get_team_score(self, match):
        home_wins = self.individualscore_set.filter(match=match, home_or_away_win='home').count()
        away_wins = self.individualscore_set.filter(match=match, home_or_away_win='away').count()
        return home_wins + away_wins