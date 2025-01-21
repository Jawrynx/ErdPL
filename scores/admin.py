from django.contrib import admin
from .models import Match, Team

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
  list_display = ('date', 'home_team', 'home_score', 'away_team', 'away_score', 'division')
  list_filter = ('date', 'division', 'home_team', 'away_team')
  search_fields = ('home_team__name', 'away_team__name')  # Search by team name
