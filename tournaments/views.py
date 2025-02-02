from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from.models import Tournament, CupGame
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def update_match_view(request, tournament_name, match_id):
    game = get_object_or_404(CupGame, pk=match_id)

    if request.method == 'POST':
        # Get the winner and scores from the form
        winner_id = request.POST.get('winner')
        score1 = request.POST.get('score1')
        score2 = request.POST.get('score2')

        # Validate the input (ensure winner is valid and scores are numbers)
        if winner_id not in [str(game.player1.id), str(game.player2.id)]:
            # Handle invalid winner selection (e.g., show an error message)
            return redirect('tournaments:update_match_view', tournament_name=tournament_name, match_id=match_id)

        try:
            score1 = int(score1)
            score2 = int(score2)
        except ValueError:
            # Handle invalid score input (e.g., show an error message)
            return redirect('tournaments:update_match_view', tournament_name=tournament_name, match_id=match_id)

        # Update the game object
        winner = get_object_or_404(User, pk=winner_id)
        game.winner = winner
        game.score1 = score1
        game.score2 = score2
        game.save()

        next_round_number = game.round_number + 1

        next_round_match, created = CupGame.objects.get_or_create(
            tournament=game.tournament,
            round_number=next_round_number,
            defaults={'player1': winner}
        )

        if not created:
            next_round_match.player2 = winner
            next_round_match.save()

        # Redirect back to the tournament page
        return redirect('tournaments:tournament_view', tournament_name=tournament_name)

    context = {
        'game': game,
        'tournament_name': tournament_name,
    }
    return render(request, 'tournaments/update_match.html', context)

def tournament_view(request, tournament_name):
    tournament = get_object_or_404(Tournament, name=tournament_name)
    games = tournament.games.order_by('round_number')

    # Organize games into rounds with specific keys
    rounds = {
        'last_32': [],
        'last_16': [],
        'quarters': [],
        'semis': [],
        'final': []
    }

    for game in games:
        if game.round_number == 1:
            rounds['last_32'].append(game)
        elif game.round_number == 2:
            rounds['last_16'].append(game)
        elif game.round_number == 3:
            rounds['quarters'].append(game)
        elif game.round_number == 4:
            rounds['semis'].append(game)
        elif game.round_number == 5:
            rounds['final'].append(game)

    context = {
        'tournament': tournament,
        'rounds': rounds,
    }
    return render(request, 'tournaments/tournament.html', context)
