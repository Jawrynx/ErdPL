from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction

from .forms import CustomUserCreationForm
from .forms import CustomUserEditForm

from .models import CustomUser
from teams.models import Team
from django.urls import reverse

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)

            username = user.username

            profile_url = reverse('users:profile', kwargs={'username': username})

            return redirect(profile_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', { "form": form })

def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)

    try:
        user_team = Team.objects.filter(members=user).first()
    except Team.DoesNotExist:
        user_team = None

    teams = Team.objects.all()

    context = {
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
    user = request.user

    if request.method == 'POST':
        user_form = CustomUserEditForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:profile', username=user.username)
        else:
            for error in user_form.errors.values():
                messages.error(request, error)

    else:  # GET request
        user_form = CustomUserEditForm(instance=user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'users/edit_profile.html', context)

@login_required
def change_password(request, username):
    user = request.user
    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 and new_password2:
            if new_password1!= new_password2:
                messages.error(request, "Passwords don't match!")
            elif password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('users:profile', username=user.username)
            else:
                for error in password_form.errors.values():
                    messages.error(request, error)
        else:
            messages.error(request, "New password fields are required.")
    else:
        password_form = PasswordChangeForm(user)

    context = {
        'password_form': password_form,
        'user': user,  # Pass the user object to the template
    }
    return render(request, 'users/change_password.html', context)