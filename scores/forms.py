from django import forms
from.models import Match, IndividualScore
from teams.models import Team
from users.models import CustomUser, Player

class MatchForm(forms.ModelForm):
    home_team = forms.ModelChoiceField(queryset=Team.objects.all())
    away_team = forms.ModelChoiceField(queryset=Team.objects.all())

    class Meta:
        model = Match
        fields = ['division', 'home_team', 'away_team', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class DirectMatchForm(forms.ModelForm):
    home_team = forms.ModelChoiceField(queryset=Team.objects.all())
    away_team = forms.ModelChoiceField(queryset=Team.objects.all())

    class Meta:
        model = Match
        fields = ['division', 'home_team', 'home_score', 'away_score', 'away_team', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class IndividualScoreForm(forms.ModelForm):
    class Meta:
        model = IndividualScore
        fields = ['home_player', 'away_player']

class IndividualPlayersForm(forms.Form):
    def __init__(self, home_team, away_team, *args, **kwargs):
        super().__init__(*args, **kwargs)
        player_x = Player.objects.get(user_id=56)
        for i in range(1, 10):
            self.fields[f'home_player_{i}'] = forms.ChoiceField(
                choices=[(player_x.id, 'X')] + [(player.id, str(player)) for player in home_team.members.all()],
                label=f'Home Player (Game {i})'
            )
            self.fields[f'away_player_{i}'] = forms.ChoiceField(
                choices=[(player_x.id, 'X')] + [(player.id, str(player)) for player in away_team.members.all()],
                label=f'Away Player (Game {i})'
            )