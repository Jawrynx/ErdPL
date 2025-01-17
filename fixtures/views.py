from django.shortcuts import render
from teams.models import Division
from .models import Fixture
from datetime import timedelta
from teams.models import Team

def fixtures_by_division(request, division_number):
    division = Division.objects.get(id=division_number)
    fixtures = Fixture.objects.filter(division=division)

    # Calculate the start and end date of each week based on the division's start date and number of weeks.
    start_date = division.start_date
    end_date = start_date + timedelta(weeks=division.num_weeks - 1)

    # Group fixtures by week
    fixtures_by_week = {}
    for week in range(1, division.num_weeks + 1):
        week_start = start_date + timedelta(weeks=week - 1)
        week_end = week_start + timedelta(days=6)
        week_fixtures = fixtures.filter(date__gte=week_start, date__lte=week_end)
        fixtures_by_week[week] = week_fixtures

    for week, fixtures in fixtures_by_week.items():
        for fixture in fixtures:
            if fixture.home_team != "X" and fixture.home_team is not None:
                fixture.home_team = Team.objects.get(name=fixture.home_team)  # Fetch Team object by name
            if fixture.away_team != "X" and fixture.away_team is not None:
                fixture.away_team = Team.objects.get(name=fixture.away_team)  # Fetch Team object by name

    context = {'division': division.name, 'fixtures_by_week': fixtures_by_week}
    return render(request, 'fixtures/fixtures_by_division.html', context)