from django.contrib import admin
from.models import Tournament, CupGame

class CupGameInline(admin.TabularInline):  
    model = CupGame
    extra = 1 

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'description')  
    search_fields = ('name', 'description') 
    inlines = [CupGameInline] 

@admin.register(CupGame)
class CupGameAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player1', 'player2', 'winner', 'round_number', 'score1', 'score2', 'date_played')
    list_filter = ('tournament', 'round_number', 'winner')
    search_fields = ('tournament__name', 'player1__username', 'player2__username') 