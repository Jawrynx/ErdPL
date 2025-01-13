from django.shortcuts import render
from teams.models import Division
from .models import Fixture

def fixtures_by_division(request, division_number):
    division = Division.objects.get(id=division_number) 
    fixtures = Fixture.objects.filter(division=division)
    context = {'fixtures': fixtures, 'division': division}
    return render(request, 'fixtures/fixtures_by_division.html', context)