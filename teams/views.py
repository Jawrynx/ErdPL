from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core import serializers

from .models import Team, Division
from scores.models import Match
from fixtures.models import Fixture
from users.models import CustomUser, Player

from .forms import TeamCreationForm, TeamEditForm

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False) 
            team.captain = request.user
            team.save()


            player = Player.objects.get(user=request.user)
            team.members.add(player) 

            selected_division_id = request.POST.get('division')
            if selected_division_id:
                division = Division.objects.get(pk=selected_division_id)
                team.division = division
                team.save()

            return redirect('teams:detail', team_name=team.name)
        else:
            return render(request, 'teams/create_team.html', {'team_creation_form': form, 'divisions': divisions})
    else:
        form = TeamCreationForm()
        divisions = Division.objects.all()
        return render(request, 'teams/create_team.html', {'team_creation_form': form, 'divisions': divisions})




@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    player = Player.objects.get(user=request.user)
    if player in team.members.all():
        return redirect('teams:detail', team_name=team.name)  # User is already a member
    team.members.add(player)
    return redirect('teams:detail', team_name=team.name)

@login_required
def leave_team(request, team_name):
    team = get_object_or_404(Team, name=team_name)
    player = Player.objects.get(user=request.user)
    if request.user == team.captain:
        return redirect('teams:detail', team_name=team.name)  # Captain cannot leave their own team
    team.members.remove(player)
    return redirect('teams:detail', team_name=team.name)

def team_detail(request, team_name):
    team = get_object_or_404(Team, name=team_name)
    team_fixtures = Fixture.objects.filter(home_team=team) | Fixture.objects.filter(away_team=team)
    team_scores = Match.objects.filter(home_team=team) | Match.objects.filter(away_team=team)

    context = {
        'team': team,
        'team_fixtures': team_fixtures,
        'team_scores': team_scores
    }
    return render(request, 'teams/team_detail.html', context)

def edit_team(request, team_name):
    team = get_object_or_404(Team, name=team_name)
    if request.user == team.captain:
        if request.method == 'POST':
            form = TeamEditForm(request.POST, request.FILES, instance=team)
            if form.is_valid():
                form.save()
                messages.success(request, 'Team information updated successfully!')
                return redirect('teams:detail', team_name=team.name)
        else:
            form = TeamEditForm(instance=team)
        return render(request, 'teams/edit_team.html', {'form': form, 'team': team})
    else:
        messages.error(request, 'You are not the captain of this team.')
        return redirect('teams:detail', team_name=team.name)

def edit_team_members(request, team_name):
    team = get_object_or_404(Team, name=team_name)

    if request.user == team.captain:
        if request.method == 'POST':
            new_member_ids = request.POST.getlist('new_members')
            for player_id in new_member_ids:
                try:
                    new_member = Player.objects.get(pk=player_id)
                    team.members.add(new_member)
                except Player.DoesNotExist:
                    pass 

            messages.success(request, 'Team members updated successfully!')
            return redirect('teams:detail', team_name=team.name)
        else:
            all_players = Player.objects.all()
            existing_member_ids = list(team.members.values_list('id', flat=True))
            available_players = all_players.exclude(id__in=existing_member_ids) 

            context = {
                'team': team,
                'available_users': available_players,
            }
            return render(request, 'teams/edit_team_members.html', context)
    else:
        messages.error(request.user, 'You are not the captain of this team.')
        return redirect('teams:team_detail', team_name=team_name)
    
def delete_team(request, team_name):
    team = get_object_or_404(Team, pk=team_name)
    if request.user == team.captain:
        team.delete()
        messages.success(request, 'Team deleted successfully!')
        return redirect('teams:team_list')  # Redirect to a team list view
    else:
        messages.error(request, 'You are not the captain of this team.')
        return redirect('teams:detail', team_name=team_name)
    
def remove_team_member(request, team_name, member_id):
    team = get_object_or_404(Team, name=team_name)
    member = get_object_or_404(Player, pk=member_id)

    if request.user == team.captain:
        if member in team.members.all():
            team.members.remove(member)
            messages.success(request, f'{member.name} removed from team.')
        else:
            messages.warning(request, f'{member.name} is not a member of this team.')
    else:
        messages.error(request, 'You are not the captain of this team.')

    return redirect('teams:edit_team_members', team_name=team_name)

@login_required
def create_player(request, team_name):
    team = get_object_or_404(Team, name=team_name)
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        player = Player.objects.create(name=player_name)

        team.members.add(player)

        return redirect('teams:edit_team_members', team_name=team.name)
    return redirect('teams:edit_team_members', team_name=team.name)