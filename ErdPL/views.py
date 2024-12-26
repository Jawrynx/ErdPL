# from django.http import HttpResponse
from django.shortcuts import render

import random

def home(request):
    teams = ['Team A', 'Team B', 'Team C', 'Team D', 'Team E', 'Team F', 'Team G', 'Team H', 'Team I', 'Team J']
    results_table = []

    for _ in range(20):
        home_team = random.choice(teams)
        away_team = random.choice(teams)
        while away_team == home_team:
            away_team = random.choice(teams)
        home_score = random.randint(0, 10)
        away_score = random.randint(0, 10)
        date = f'2024-12-{random.randint(1, 31)}'  # Generate random dates in December 2024

        results_table.append({
            'home_team': home_team,
            'away_team': away_team,
            'home_score': home_score,
            'away_score': away_score,
            'date': date
        })

    context = {'results_table': results_table}
    return render(request, 'home.html', context)

def about(request):
    # return HttpResponse('Hello, I am the About Page!')
    return render(request, 'about.html')

def contact(request):
    # return HttpResponse('Hello, I am the Contact Page!')
    return render(request, 'contact.html')