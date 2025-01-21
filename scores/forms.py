from django import forms
from .models import Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_team', 'home_score', 'away_team', 'away_score', 'date'] 