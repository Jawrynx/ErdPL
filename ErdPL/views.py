from django.shortcuts import render, get_object_or_404
from teams.models import Team, Division
from scores.models import Match

def calculate_leaderboard(division):
    """
    Calculates the leaderboard for a given division.

    Args:
        division (Division): The division object.

    Returns:
        list: A list of dictionaries, where each dictionary represents a team's 
              standing with its name, wins, losses, and points.
    """

    teams = Team.objects.filter(division=division)
    leaderboard = []

    for team in teams:
        wins = 0
        losses = 0
        points = 0  # Initialize points here
        played = 0
        frames_won = 0
        frames_lost = 0

        # Calculate home matches
        home_matches = Match.objects.filter(home_team=team, division=division)
        for match in home_matches:
            played += 1
            frames_won += match.home_score
            frames_lost += match.away_score
            if match.home_score > match.away_score:
                wins += 1
            else:
                losses += 1

        # Calculate away matches
        away_matches = Match.objects.filter(away_team=team, division=division)
        for match in away_matches:
            played += 1
            frames_won += match.away_score
            frames_lost += match.home_score
            if match.away_score > match.home_score:
                wins += 1
            else:
                losses += 1

        points = frames_won
        bonus_points = wins * 3
        points += bonus_points


        leaderboard.append({
            'team': team,
            'wins': wins,
            'losses': losses,
            'played': played,
            'frames_won': frames_won,
            'frames_lost': frames_lost,
            'bonus_points': bonus_points,
            'points': points
        })

    # Sort the leaderboard by points (descending)
    leaderboard.sort(key=lambda x: (-x['points'], -x['wins']))

    return leaderboard


def home(request):
    all_divisions = Division.objects.all()

    # Pre-defined order of divisions
    division_order = ["Premier Division", "Division One", "Division Two"]
    ordered_divisions = []

    # Add divisions in the specified order first
    for division_name in division_order:
        try:
            division = all_divisions.get(name=division_name)  # Use.get() for single object
            division.leaderboard = calculate_leaderboard(division)
            ordered_divisions.append(division)
        except Division.DoesNotExist:
            pass # Handle if division doesn't exist

    # Add remaining divisions (if any) alphabetically
    other_divisions = []
    for division in all_divisions:
        if division.name not in division_order:
            other_divisions.append(division)

    other_divisions.sort(key=lambda x: x.name) # Sort alphabetically
    for division in other_divisions:
      division.leaderboard = calculate_leaderboard(division)
      ordered_divisions.append(division)

    context = {
        'all_divisions': ordered_divisions,  # Use the ordered list
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')