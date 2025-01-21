from django.shortcuts import render, redirect, get_object_or_404
from .models import Match, Team, Division
from .forms import MatchForm

def create_score(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scores:view_scores')  # Redirect to a view to display scores
    else:
        form = MatchForm()
    return render(request, 'scores/create_score.html', {'form': form})

def view_scores(request, division_name=None):
    all_divisions = Division.objects.all()

    if division_name:
        matches = Match.objects.filter(division__name=division_name).order_by('-date')
    else:
        matches = Match.objects.all().order_by('-date') 

    context = {
        'matches': matches,
        'division_name': division_name,
        'all_divisions': all_divisions,
    }
    return render(request, 'scores/view_scores.html', context)