from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from .models import Profile, CustomUser
from django.urls import reverse

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)

            Profile.objects.create(user=user)

            username = user.username

            profile_url = reverse('users:profile', kwargs={'username': username})

            return redirect(profile_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', { "form": form })

def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    profile = user.profile

    return render(request, 'users/profile.html', {'profile': profile})

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