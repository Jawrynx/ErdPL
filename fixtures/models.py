from django.db import models
from teams.models import Team, Division 

class Fixture(models.Model):
    home_team = models.CharField(max_length=255, null=True, blank=True)
    away_team = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    bye_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='bye_fixtures')

    def __str__(self):
        if self.bye_team:
            return f"{self.home_team} vs BYE on {self.date}"
        elif self.away_team:
            return f"{self.home_team} vs {self.away_team} on {self.date}"
        else:
            return f"BYE vs {self.away_team} on {self.date}"