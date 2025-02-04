from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tournament(models.Model):
    name = models.CharField(max_length=255, unique=True)
    start_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tournament_winner', null=True, blank=True)

    def __str__(self):
        return self.name

class Last32Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='last_32_matches')
    player1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='last_32_matches_as_player1', null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='last_32_matches_as_player2', null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='last_32_matches_won', null=True, blank=True)
    score1 = models.PositiveIntegerField(null=True, blank=True)
    score2 = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player1.username if self.player1 else 'TBD'} vs {self.player2.username if self.player2 else 'TBD'}"

class Last16Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='last_16_matches')
    player1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='last_16_matches_as_player1', null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='last_16_matches_as_player2', null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='last_16_matches_won', null=True, blank=True)
    score1 = models.PositiveIntegerField(null=True, blank=True)
    score2 = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player1.username if self.player1 else 'TBD'} vs {self.player2.username if self.player2 else 'TBD'}"

class QuarterFinalMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='quarter_final_matches')
    player1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='quarter_final_matches_as_player1', null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='quarter_final_matches_as_player2', null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='quarter_final_matches_won', null=True, blank=True)
    score1 = models.PositiveIntegerField(null=True, blank=True)
    score2 = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player1.username if self.player1 else 'TBD'} vs {self.player2.username if self.player2 else 'TBD'}"

class SemiFinalMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='semi_final_matches')
    player1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='semi_final_matches_as_player1', null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='semi_final_matches_as_player2', null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='semi_final_matches_won', null=True, blank=True)
    score1 = models.PositiveIntegerField(null=True, blank=True)
    score2 = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player1.username if self.player1 else 'TBD'} vs {self.player2.username if self.player2 else 'TBD'}"

class FinalMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='final_matches')
    player1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='final_matches_as_player1', null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='final_matches_as_player2', null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='final_matches_won', null=True, blank=True)
    score1 = models.PositiveIntegerField(null=True, blank=True)
    score2 = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player1.username if self.player1 else 'TBD'} vs {self.player2.username if self.player2 else 'TBD'}"