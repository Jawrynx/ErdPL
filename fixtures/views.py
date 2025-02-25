from django.shortcuts import render
from teams.models import Division
from .models import Fixture
from datetime import timedelta
from teams.models import Team

def fixtures_by_division(request, division_name):
    division = Division.objects.get(name=division_name)
    fixtures = Fixture.objects.filter(division=division).order_by('date')
    all_divisions = Division.objects.all()

    #Order Divisions by Highest Ranking

    correct_order = ['Premier Division', 'Division 1', 'Division 2']
    ordered_divisions = []

    for item in correct_order:
        for division in all_divisions:
            if item == division.name:
                ordered_divisions.append(division)

    print(ordered_divisions)

    # Group fixtures by week, considering gaps
    fixtures_by_week = {}
    week_number = 1
    current_week_start = fixtures.first().date  # Start with the first fixture's date
    current_week_end = current_week_start + timedelta(days=6)

    for fixture in fixtures:
        if fixture.date > current_week_end:  # Move to the next week
            week_number += 1
            current_week_start = fixture.date
            current_week_end = current_week_start + timedelta(days=6)

        # Add fixture to the current week
        if week_number not in fixtures_by_week:
            fixtures_by_week[week_number] = []
        fixtures_by_week[week_number].append(fixture)
    
    teams = Team.objects.all()

    context = {
        'division': division_name,
        'fixtures_by_week': fixtures_by_week,
        'all_divisions': ordered_divisions,
        'teams': teams,
    }
    return render(request, 'fixtures/fixtures_by_division.html', context)