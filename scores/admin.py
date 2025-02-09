from django.contrib import admin
from .models import Match, Team, IndividualScore

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
  list_display = ('date', 'home_team', 'home_score', 'away_team', 'away_score', 'division')
  list_filter = ('date', 'division', 'home_team', 'away_team')
  search_fields = ('home_team__name', 'away_team__name')  # Search by team name

class IndividualScoreAdmin(admin.ModelAdmin):
    list_display = ('match', 'home_player', 'away_player', 'home_or_away_win')
    list_filter = ('match', 'home_player', 'away_player', 'home_or_away_win')
    search_fields = ('match__home_team__name', 'match__away_team__name', 'home_player__username', 'away_player__username')  # Assuming 'name' field in Team and 'username' in CustomUser

    # Add fields for editing in the admin panel (optional)
    fields = ('match', 'home_player', 'away_player', 'home_or_away_win')

# Register the model with the admin site
admin.site.register(IndividualScore, IndividualScoreAdmin)