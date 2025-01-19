from django.shortcuts import render
from teams.models import Division
from .models import Fixture
from datetime import timedelta
from teams.models import Team

def fixtures_by_division(request, division_name):
    division = Division.objects.get(name=division_name)
    fixtures = Fixture.objects.filter(division=division).order_by('date')
    all_divisions = Division.objects.all()

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

    context = {'division': division.name, 'fixtures_by_week': fixtures_by_week, 'all_divisions': all_divisions}
    return render(request, 'fixtures/fixtures_by_division.html', context)