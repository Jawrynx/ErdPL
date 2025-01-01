from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from .models import Profile
from django.urls import reverse

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)

            Profile.objects.create(user=user)

            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', { "form": form })

def profile_view(request):
    user = request.user
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