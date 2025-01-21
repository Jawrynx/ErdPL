from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm
from .forms import ProfileEditForm

from .models import Profile, CustomUser
from teams.models import Team
from django.urls import reverse

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)

            profile = Profile.objects.create(
                user=user,
                fullname=request.POST.get('fullname', ''), 
                profile_picture=request.FILES.get('profile_picture', None), 
                phone_number=request.POST.get('phone_number', ''), 
                bio=request.POST.get('bio', '')
            )

            username = user.username

            profile_url = reverse('users:profile', kwargs={'username': username})

            return redirect(profile_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', { "form": form })

def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    profile = user.profile

    try:
        user_team = Team.objects.filter(members=user).first()
    except Team.DoesNotExist:
        user_team = None

    teams = Team.objects.all()

    context = {
        'profile': profile,
        'user_team': user_team,
        'teams': teams,
    }

    return render(request, 'users/profile.html', context)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', { "form": form })

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def edit_profile(request, username):
    if request.method == 'POST':
        user = request.user  # Get the current user
        profile = user.profile
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('users:profile', username=user)

    else:
        user = request.user
        profile = user.profile
        form = ProfileEditForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'users/edit_profile.html', context)