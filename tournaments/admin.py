from django.contrib import admin
from.models import Tournament, Last32Match, Last16Match, QuarterFinalMatch, SemiFinalMatch, FinalMatch

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'description')
    search_fields = ('name', 'description')

@admin.register(Last32Match)
class Last32MatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player1', 'player2', 'winner', 'score1', 'score2')
    list_filter = ('tournament', 'winner')
    search_fields = ('tournament__name', 'player1__username', 'player2__username')

@admin.register(Last16Match)
class Last16MatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player1', 'player2', 'winner', 'score1', 'score2')
    list_filter = ('tournament', 'winner')
    search_fields = ('tournament__name', 'player1__username', 'player2__username')

@admin.register(QuarterFinalMatch)
class QuarterFinalMatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player1', 'player2', 'winner', 'score1', 'score2')
    list_filter = ('tournament', 'winner')
    search_fields = ('tournament__name', 'player1__username', 'player2__username')

@admin.register(SemiFinalMatch)
class SemiFinalMatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player1', 'player2', 'winner', 'score1', 'score2')
    list_filter = ('tournament', 'winner')
    search_fields = ('tournament__name', 'player1__username', 'player2__username')

@admin.register(FinalMatch)
class FinalMatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player1', 'player2', 'winner', 'score1', 'score2')
    list_filter = ('tournament', 'winner')
    search_fields = ('tournament__name', 'player1__username', 'player2__username')