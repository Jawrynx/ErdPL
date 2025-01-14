from django import forms
from .models import Team

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class TeamEditForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'bio', 'team_image'] 