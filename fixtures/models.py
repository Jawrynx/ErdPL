from django.db import models
from teams.models import Team, Division 

class Fixture(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_fixtures')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_fixtures')
    date = models.DateField()
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    HOME_AWAY_CHOICES = [('HOME', 'Home'), ('AWAY', 'Away'),]
    home_or_away = models.CharField(max_length=5, choices=HOME_AWAY_CHOICES, default='HOME')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"