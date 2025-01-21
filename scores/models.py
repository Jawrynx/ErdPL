from django.db import models
from django.contrib.auth.models import AbstractUser
from teams.models import Team, Division

class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    home_score = models.PositiveIntegerField()
    away_score = models.PositiveIntegerField()
    date = models.DateField()
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.date})"