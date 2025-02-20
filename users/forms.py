from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'fullname', 'phone_number') 

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'fullname', 'profile_picture', 'phone_number', 'bio']

    username = forms.CharField(required=False)