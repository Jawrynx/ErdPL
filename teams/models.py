from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Division(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name='captain_of')
    members = models.ManyToManyField(User, related_name='teams')
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True) 

    def __str__(self):
        return self.name