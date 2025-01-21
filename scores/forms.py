from django import forms
from .models import Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_team', 'away_team', 'home_score', 'away_score', 'date', 'division']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Use a date picker
        }