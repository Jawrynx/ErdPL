from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core import serializers
import json

from .models import Team, Division
from fixtures.models import Fixture
from users.models import CustomUser

from .forms import TeamCreationForm, TeamEditForm

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
    team_fixtures = Fixture.objects.filter(home_team=team) | Fixture.objects.filter(away_team=team)
    context = {'team': team, 'team_fixtures': team_fixtures}
    return render(request, 'teams/team_detail.html', context) 

def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user == team.captain:
        if request.method == 'POST':
            form = TeamEditForm(request.POST, instance=team)
            if form.is_valid():
                form.save()
                messages.success(request, 'Team information updated successfully!')
                return redirect('teams:detail', team_id=team_id)
        else:
            form = TeamEditForm(instance=team)
        return render(request, 'teams/edit_team.html', {'form': form, 'team': team})
    else:
        messages.error(request, 'You are not the captain of this team.')
        return redirect('teams:detail', team_id=team_id)

def edit_team_members(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    CustomUser = get_user_model()

    if request.user == team.captain:
        if request.method == 'POST':
            # Get the list of user IDs from the POST data
            new_member_ids = request.POST.getlist('new_members') 

            # Remove existing members (if any)

            # Add new members to the team
            for user_id in new_member_ids:
                try:
                    new_member = CustomUser.objects.get(pk=user_id)
                    team.members.add(new_member)
                except CustomUser.DoesNotExist:
                    pass 

            messages.success(request, 'Team members updated successfully!')
            return redirect('teams:detail', team_id=team_id)
        else:
            # Get a list of all users 
            all_users = CustomUser.objects.all()

            # Get a list of users who are not already members of the team
            existing_member_ids = list(team.members.values_list('id', flat=True))
            available_users = all_users.exclude(id__in=existing_member_ids) 

            context = {
                'team': team,
                'available_users': available_users 
            }
            return render(request, 'teams/edit_team_members.html', context)
    else:
        messages.error(request.user, 'You are not the captain of this team.')
        return redirect('teams:team_detail', team_id=team_id)
    
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user == team.captain:
        team.delete()
        messages.success(request, 'Team deleted successfully!')
        return redirect('teams:team_list')  # Redirect to a team list view
    else:
        messages.error(request, 'You are not the captain of this team.')
        return redirect('teams:detail', team_id=team_id)
    
def remove_team_member(request, team_id, member_id):
    team = get_object_or_404(Team, pk=team_id)
    member = get_object_or_404(CustomUser, pk=member_id)

    if request.user == team.captain:
        if member in team.members.all():
            team.members.remove(member)
            messages.success(request, f'{member.username} removed from team.')
        else:
            messages.warning(request, f'{member.username} is not a member of this team.')
    else:
        messages.error(request, 'You are not the captain of this team.')

    return redirect('teams:edit_team_members', team_id=team_id)