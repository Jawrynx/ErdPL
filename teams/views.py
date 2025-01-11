from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Team, Division
from .forms import TeamCreationForm  

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False) 
            team.captain = request.user
            team.save()
            team.members.add(request.user) 

            selected_division_id = request.POST.get('division')
            if selected_division_id:
                division = Division.objects.get(pk=selected_division_id)
                team.division = division
                team.save()

            return redirect('teams:detail', team_id=team.id)
        else:
            return render(request, 'teams/create_team.html', {'team_creation_form': form, 'divisions': divisions})
    else:
        form = TeamCreationForm()
        divisions = Division.objects.all()
        return render(request, 'teams/create_team.html', {'team_creation_form': form, 'divisions': divisions})




@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user in team.members.all():
        return redirect('teams:detail', team_id=team_id)  # User is already a member
    team.members.add(request.user)
    return redirect('teams:detail', team_id=team_id)

@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user == team.captain:
        return redirect('teams:detail', team_id=team_id)  # Captain cannot leave their own team
    team.members.remove(request.user)
    return redirect('teams:detail', team_id=team_id)

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id) 
    context = {'team': team}
    return render(request, 'teams/team_detail.html', context) 