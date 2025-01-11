from django.shortcuts import render
from teams.models import Division
from .models import Fixture

def fixtures_home(request):
    division_1 = Division.objects.get(name="Division 1") 
    fixtures = Fixture.objects.filter(division=division_1)
    context = {'fixtures': fixtures, 'division': division_1}
    return render(request, 'fixtures/fixtures_home.html', context)