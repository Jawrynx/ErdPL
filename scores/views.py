from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from.models import Match, IndividualScore, Team, Division
from.forms import MatchForm, IndividualScoreForm, IndividualPlayersForm
from users.models import CustomUser

def create_score(request, division_name=None):
    if division_name:
        try:
            division = Division.objects.get(name=division_name)
        except Division.DoesNotExist:
            return redirect('scores:view_scores')

    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.division = division
            match.save()
            return redirect('scores:select_players', division_name=division_name, match_id=match.id)
    else:
        form = MatchForm()
        # Create a list of IndividualScoreForms for each game
        score_forms = [IndividualScoreForm() for _ in range(9)]
    return render(request, 'scores/create_score.html', {'form': form, 'division_name': division_name, 'score_forms': score_forms})

def select_players(request, match_id, division_name):
    match = get_object_or_404(Match, pk=match_id)
    existing_scores = IndividualScore.objects.filter(match=match)
    if existing_scores.exists():
        # Redirect to live_match if scores already exist
        return redirect('scores:live_match', division_name=division_name, match_id=match.id)

    if request.method == 'POST':
        form = IndividualPlayersForm(match.home_team, match.away_team, request.POST)
        if form.is_valid():
            for i in range(1, 10):
                home_player_id = form.cleaned_data.get(f'home_player_{i}')
                away_player_id = form.cleaned_data.get(f'away_player_{i}')

                # Convert player IDs to CustomUser objects or None
                home_player = CustomUser.objects.get(pk=home_player_id) if home_player_id!= 'X' else None
                away_player = CustomUser.objects.get(pk=away_player_id) if away_player_id!= 'X' else None

                IndividualScore.objects.create(
                    match=match,
                    home_player=home_player,
                    away_player=away_player
                )
            return redirect('scores:live_match', division_name=division_name, match_id=match.id)
        
    else:
        form = IndividualPlayersForm(match.home_team, match.away_team)
    return render(request, 'scores/select_players.html', {'form': form, 'match': match})
def live_match(request, match_id, division_name):
    match = get_object_or_404(Match, pk=match_id)
    scores = IndividualScore.objects.filter(match=match)
    return render(request, 'scores/live_match.html', {'match': match, 'scores': scores})

def update_score(request, division_name, match_id, score_id):
    # Get the match and score objects using the provided IDs
    match = get_object_or_404(Match, pk=match_id)
    score = get_object_or_404(IndividualScore, pk=score_id)

    # Update the score
    winner = request.POST.get('winner')
    score.home_or_away_win = winner
    score.save()

    if winner == 'home':
        match.home_score += 1
    elif winner == 'away':
        match.away_score += 1
    match.save()

    return redirect('scores:live_match', division_name=division_name, match_id=match.id)

def view_scores(request, division_name=None):
    all_divisions = Division.objects.all()
    if division_name:
        matches = Match.objects.filter(division__name=division_name).order_by('-date')
        teams = Team.objects.filter(division__name=division_name)
    else:
        matches = Match.objects.all().order_by('-date')
        teams = Team.objects.all()
    context = {
        'matches': matches,
        'division_name': division_name,
        'all_divisions': all_divisions,
        'teams': teams,
    }
    return render(request, 'scores/view_scores.html', context)

def match_details(request, division_name, match_id):
    match = get_object_or_404(Match, pk=match_id)
    context = {
        'match': match,
        'division_name': division_name,
        'home_team': match.home_team,
        'away_team': match.away_team,
    }
    return render(request, 'scores/match_details.html', context)