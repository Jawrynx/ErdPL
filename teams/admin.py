from django.contrib import admin
from .models import Team, Division

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_image', 'captain', 'division') 
    list_filter = ('division',) 

admin.site.register(Team, TeamAdmin)
admin.site.register(Division)