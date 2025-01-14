from django import forms
from .models import Team

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'location', 'bio']

class TeamEditForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_image', 'name', 'location', 'bio'] 
        
    def __init__(self, *args, **kwargs):
        super(TeamEditForm, self).__init__(*args, **kwargs)
        self.fields['team_image'].required = False 