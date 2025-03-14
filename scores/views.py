from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from.models import Match, IndividualScore, Team, Division
from.forms import MatchForm, IndividualScoreForm, IndividualPlayersForm, DirectMatchForm
from users.models import CustomUser, Player

def create_score(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            division = match.division
            match.save()
            return redirect('scores:select_players', division_name=division, match_id=match.id)
    else:
        form = MatchForm()
        # Create a list of IndividualScoreForms for each game
        score_forms = [IndividualScoreForm() for _ in range(9)]
    return render(request, 'scores/create_score.html', {'form': form, 'score_forms': score_forms})

def add_match_score(request):
    if request.method == 'POST':
        form = DirectMatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            division = match.division
            match.save()
            return redirect('scores:view_scores', division_name=division)
    else:
        form = DirectMatchForm()

    return render(request, 'scores/add_match_score.html', {'form': form})

def select_players(request, division_name, match_id):
    match = get_object_or_404(Match, id=match_id)
    existing_scores = IndividualScore.objects.filter(match=match)
    home_team = match.home_team
    away_team = match.away_team

    if request.method == 'POST':
        form = IndividualPlayersForm(home_team, away_team, request.POST)
        if form.is_valid():
            for i in range(1, 10):
                home_player_id = form.cleaned_data.get(f'home_player_{i}')
                away_player_id = form.cleaned_data.get(f'away_player_{i}')

                print(home_player_id)

                home_player = None
                away_player = None

                if home_player_id != 'X':
                    try:
                        home_player = Player.objects.get(pk=home_player_id)
                    except Player.DoesNotExist:
                        print(f"Warning: Home Player with ID {home_player_id} does not exist.")
                        #Handle the error, for now just skip to the next loop.
                        continue

                if away_player_id != 'X':
                    try:
                        away_player = Player.objects.get(pk=away_player_id)
                    except Player.DoesNotExist:
                        print(f"Warning: Away Player with ID {away_player_id} does not exist.")
                        #Handle the error, for now just skip to the next loop.
                        continue

                IndividualScore.objects.create(
                    match=match,
                    home_player=home_player,
                    away_player=away_player
                )
            return redirect('scores:live_match', division_name=division_name, match_id=match.id)
    else:
        form = IndividualPlayersForm(home_team, away_team)

    context = {
        'form': form,
        'match': match,
        'existing_scores': existing_scores,
    }
    return render(request, 'scores/select_players.html', context)



def live_match(request, match_id, division_name):
    match = get_object_or_404(Match, pk=match_id)
    scores = IndividualScore.objects.filter(match=match).order_by('id')
    return render(request, 'scores/live_match.html', {'match': match, 'scores': scores})

def update_score(request, division_name, match_id, score_id):
    # Get the match and score objects using the provided IDs
    match = get_object_or_404(Match, pk=match_id)
    score = get_object_or_404(IndividualScore, pk=score_id)
    home_player = score.home_player
    away_player = score.away_player

    # Update the score
    winner = request.POST.get('winner')
    score.home_or_away_win = winner
    score.save()

    if winner == 'home':
        match.home_score += 1
        home_player.game_wins += 1
        away_player.game_losses += 1
    elif winner == 'away':
        match.away_score += 1
        away_player.game_wins += 1
        home_player.game_losses += 1
    match.save()

    return redirect('scores:live_match', division_name=division_name, match_id=match.id)

def view_scores(request, division_name=None):
    all_divisions = Division.objects.all()

    correct_order = ['Premier Division', 'Division 1', 'Division 2']
    ordered_divisions = []

    for item in correct_order:
        for division in all_divisions:
            if item == division.name:
                ordered_divisions.append(division)

    print(ordered_divisions)

    if division_name:
        matches = Match.objects.filter(division__name=division_name).order_by('-date')
        teams = Team.objects.filter(division__name=division_name)
    else:
        matches = Match.objects.all().order_by('-date')
        teams = Team.objects.all()
    context = {
        'matches': matches,
        'division_name': division_name,
        'all_divisions': ordered_divisions,
        'teams': teams,
    }
    return render(request, 'scores/view_scores.html', context)

def match_details(request, division_name, match_id):
    match = get_object_or_404(Match, pk=match_id)
    match_scores = []
    all_scores = IndividualScore.objects.all()

    for score in all_scores:
        if score.match.id == match_id:
            match_scores.append(score)
        else:
            continue

    match_scores_sorted = sorted(match_scores, key=lambda x: x.id)

    context = {
        'match': match,
        'division_name': division_name,
        'home_team': match.home_team,
        'away_team': match.away_team,
        'scores': match_scores_sorted,
    }
    return render(request, 'scores/match_details.html', context)