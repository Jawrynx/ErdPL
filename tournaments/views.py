from django.shortcuts import render, get_object_or_404
from.models import Tournament, CupGame

def tournament_view(request, tournament_name):
    tournament = get_object_or_404(Tournament, name=tournament_name)
    games = tournament.games.order_by('round_number')

    # Organize games into rounds for display in the template
    rounds = {}
    for game in games:
        if game.round_number not in rounds:
            rounds[game.round_number] = []
        rounds[game.round_number].append(game)

    context = {
        'tournament': tournament,
        'rounds': rounds,
    }
    return render(request, 'tournaments/tournament.html', context)