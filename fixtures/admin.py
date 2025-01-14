from django.contrib import admin
from .models import Fixture

class FixtureAdmin(admin.ModelAdmin):
    list_display = ('date', 'home_team', 'away_team', 'division') 
    list_filter = ('division', 'date') 
    date_hierarchy = 'date' 

admin.site.register(Fixture, FixtureAdmin)