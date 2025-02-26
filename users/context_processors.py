from users.models import Player
from teams.models import Team

def user_team_context(request):
    user_team = None
    if request.user.is_authenticated:
        try:
            player = Player.objects.get(user=request.user)
            user_team = Team.objects.filter(members=player).first()
        except Player.DoesNotExist:
            pass

    return {'user_team': user_team}