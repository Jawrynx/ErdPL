from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'fullname', 'phone_number') 

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'profile_picture', 'phone_number', 'bio']

class UsernameEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

    username = forms.CharField(required=False)