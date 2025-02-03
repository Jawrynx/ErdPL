from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from.models import Tournament, Last32Match, Last16Match, QuarterFinalMatch, SemiFinalMatch, FinalMatch
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def update_match_view(request, tournament_name, match_id, round_name):
    if round_name == 'last_32':
        game = get_object_or_404(Last32Match, pk=match_id)
    elif round_name == 'last_16':
        game = get_object_or_404(Last16Match, pk=match_id)
    elif round_name == 'quarters':
        game = get_object_or_404(QuarterFinalMatch, pk=match_id)
    elif round_name == 'semis':
        game = get_object_or_404(SemiFinalMatch, pk=match_id)
    elif round_name == 'final':
        game = get_object_or_404(FinalMatch, pk=match_id)
    else:
        raise ValueError("Invalid round name")

    if request.method == 'POST':
        # Get the winner and scores from the form
        winner_id = request.POST.get('winner')
        score1 = request.POST.get('score1')
        score2 = request.POST.get('score2')

        # Validate the input (ensure winner is valid and scores are numbers)
        if winner_id not in [str(game.player1.id), str(game.player2.id)]:
            # Handle invalid winner selection (e.g., show an error message)
            return redirect('tournaments:update_match_view', tournament_name=tournament_name, match_id=match_id, round_name=round_name)  # Added round_name

        try:
            score1 = int(score1)
            score2 = int(score2)
        except ValueError:
            # Handle invalid score input (e.g., show an error message)
            return redirect('tournaments:update_match_view', tournament_name=tournament_name, match_id=match_id, round_name=round_name)  # Added round_name

        # Update the game object
        winner = get_object_or_404(User, pk=winner_id)
        game.winner = winner
        game.score1 = score1
        game.score2 = score2
        game.save()

        # Update the next round match (if applicable)
        if round_name == 'last_32':
            next_match_id = (match_id + 1) // 2
            try:
                next_match = Last16Match.objects.get(pk=next_match_id)
                if next_match.player1 is None:
                    next_match.player1 = winner
                else:
                    next_match.player2 = winner
                next_match.save()
            except Last16Match.DoesNotExist:
                pass  # Or handle the case where the next match doesn't exist
        elif round_name == 'last_16':
            next_match_id = (match_id + 1) // 2
            try:
                next_match = QuarterFinalMatch.objects.get(pk=next_match_id)
                if next_match.player1 is None:
                    next_match.player1 = winner
                else:
                    next_match.player2 = winner
                next_match.save()
            except QuarterFinalMatch.DoesNotExist:
                pass  # Or handle the case where the next match doesn't exist
        #... similar logic for other rounds...

        # Redirect back to the tournament page
        return redirect('tournaments:tournament_view', tournament_name=tournament_name)

    context = {
        'game': game,
        'tournament_name': tournament_name,
        'round_name': round_name,  # Pass the round name to the template
    }
    return render(request, 'tournaments/update_match.html', context)

def tournament_view(request, tournament_name):
    tournament = get_object_or_404(Tournament, name=tournament_name)

    # Get all matches for each round
    last_32_matches = Last32Match.objects.filter(tournament=tournament)
    last_16_matches = Last16Match.objects.filter(tournament=tournament)
    quarter_final_matches = QuarterFinalMatch.objects.filter(tournament=tournament)
    semi_final_matches = SemiFinalMatch.objects.filter(tournament=tournament)
    final_match = FinalMatch.objects.filter(tournament=tournament).first()  # Get the first (and only) FinalMatch object

    # Organize matches into rounds
    rounds = {
        'last_32': last_32_matches,
        'last_16': last_16_matches,
        'quarters': quarter_final_matches,
        'semis': semi_final_matches,
        'final': final_match,  # Pass the FinalMatch object directly
    }

    # Create a list of all players in the tournament
    players = set()
    for match_list in rounds.values():
        if isinstance(match_list, list):  # Check if it's a list of matches
            for match in match_list:
                players.add(match.player1)
                if match.player2:
                    players.add(match.player2)
        elif isinstance(match_list, FinalMatch):  # Handle the final match separately
            players.add(match_list.player1)
            if match_list.player2:
                players.add(match_list.player2)

    # Create a dictionary to store player names by ID
    player_names = {player.id: player.username for player in players if player}

    context = {
        'tournament': tournament,
        'rounds': rounds,
        'players': players,
        'player_names': player_names,
    }
    return render(request, 'tournaments/tournament.html', context)