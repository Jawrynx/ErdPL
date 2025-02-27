from django.db import models
from django.contrib.auth.models import AbstractUser
from teams.models import Team, Division
from users.models import CustomUser, Player

class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    date = models.DateField()
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.date})"
    
class IndividualScore(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='home_scores', null=True, blank=True)
    away_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='away_scores', null=True, blank=True)
    home_or_away_win = models.CharField(max_length=5, choices=[('home', 'Home'), ('away', 'Away')])

    def __str__(self):
        return f"{self.match} - {self.home_player} vs {self.away_player}"