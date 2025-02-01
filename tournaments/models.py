from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tournament(models.Model):
    name = models.CharField(max_length=255, unique=True)  
    start_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CupGame(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='games')
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1_games')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2_games', null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='winning_games')
    round_number = models.PositiveIntegerField()
    # Add other fields as needed (e.g., score, date_played)
    score1 = models.PositiveIntegerField(null=True, blank=True)
    score2 = models.PositiveIntegerField(null=True, blank=True)
    date_played = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.player1.username} vs {self.player2.username if self.player2 else 'TBD'} (Round {self.round_number})"

    class Meta:
        unique_together = ('tournament', 'player1', 'player2', 'round_number') # prevent duplicate matches