# from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse('Hello, I am working!')
    return render(request, 'home.html')

def about(request):
    # return HttpResponse('Hello, I am the About Page!')
    return render(request, 'about.html')

def contact(request):
    # return HttpResponse('Hello, I am the Contact Page!')
    return render(request, 'contact.html')