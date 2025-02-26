from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True)
    team = models.OneToOneField('teams.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')

    def __str__(self):
        return self.username 

class Player(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, default='')
    match_wins = models.IntegerField(null=True, default=0)
    match_losses = models.IntegerField(null=True, default=0)
    game_wins = models.IntegerField(null=True, default=0)
    game_losses = models.IntegerField(null=True, default=0)
    total_games = models.IntegerField(null=True, default=0)
    win_to_loss_ratio = models.CharField(null=True, default='0:0', max_length=10)