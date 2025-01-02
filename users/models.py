from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username 

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Use CustomUser here
    fullname = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_default.jpeg')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username