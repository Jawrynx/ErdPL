from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from.models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'fullname', 'profile_picture', 'phone_number', 'bio', 'get_team') 

    def get_team(self, obj):
        if obj.team:
            return obj.team.name 
        return "No team"

    get_team.short_description = 'Team' 

admin.site.register(CustomUser, CustomUserAdmin)