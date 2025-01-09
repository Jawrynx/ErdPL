from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import CustomUser

# Register your custom user model with the admin panel
admin.site.register(CustomUser, BaseUserAdmin)

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'get_teams')

    def get_teams(self, obj):
        return ", ".join([team.name for team in obj.teams.all()]) 
    get_teams.short_description = 'Teams'

# Register the customized admin view for CustomUser
admin.site.unregister(CustomUser)  # Unregister previous registration (if any)
admin.site.register(CustomUser, CustomUserAdmin) 