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
