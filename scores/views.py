from django.shortcuts import render, redirect, get_object_or_404
from .models import Match, Team, Division
from .forms import MatchForm

def create_score(request, division_name=None):
    if division_name:
        try:
            division = Division.objects.get(name=division_name)
        except Division.DoesNotExist:
            # Handle the case where the division doesn't exist
            return redirect('scores:view_scores')  # Or display an error message

    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.division = division
            match.save()
            return redirect('scores:view_scores', division_name=division_name)
    else:
        form = MatchForm()
    return render(request, 'scores/create_score.html', {'form': form, 'division_name': division_name})

def view_scores(request, division_name=None):
    all_divisions = Division.objects.all()

    if division_name:
        matches = Match.objects.filter(division__name=division_name).order_by('-date')
        # Get teams associated with the division
        teams = Team.objects.filter(division__name=division_name) 
    else:
        matches = Match.objects.all().order_by('-date')
        # Get all teams
        teams = Team.objects.all()

    context = {
        'matches': matches,
        'division_name': division_name,
        'all_divisions': all_divisions,
        'teams': teams, 
    }
    return render(request, 'scores/view_scores.html', context)