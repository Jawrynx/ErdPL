from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction

from .forms import CustomUserCreationForm
from .forms import ProfileEditForm
from .forms import UsernameEditForm

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
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        username_form = UsernameEditForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)  # Initialize here, but don't use it unconditionally

        if profile_form.is_valid() and username_form.is_valid():
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if new_password1 and new_password2:  # Check if BOTH new password fields are filled
                if new_password1!= new_password2:
                    messages.error(request, "Passwords don't match!")
                elif password_form.is_valid():  # Only validate/save if new passwords provided
                    user = password_form.save()
                    update_session_auth_hash(request, user)
                    profile_form.save()
                    username_form.save()
                    messages.success(request, 'Your profile and password were successfully updated!')
                    return redirect('users:profile', username=user.username)
                else:
                    for error in password_form.errors.values():
                        messages.error(request, error)  # Display password form errors
            else:  # No new password provided, just save profile and username
                 with transaction.atomic():
                    profile_form.save()
                    username_form.save()
                 messages.success(request, 'Your profile was successfully updated!')
                 return redirect('users:profile', username=user.username)
        else:
            for error in profile_form.errors.values():
                messages.error(request, error)
            for error in username_form.errors.values():
                messages.error(request, error)

    else:  # GET request
        profile_form = ProfileEditForm(instance=profile)
        username_form = UsernameEditForm(instance=user)
        password_form = PasswordChangeForm(user) # Important: Initialize even on GET for CSRF

    context = {
        'profile_form': profile_form,
        'username_form': username_form,
        'profile': profile,
        'password_form': password_form,  # Add password form to the context
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