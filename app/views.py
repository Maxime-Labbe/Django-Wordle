from django.shortcuts import render
from django.http import HttpResponse
from . import robot

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def solo(request):
    return render(request, 'app/solo.html')

def robot_view(request):
    data = robot.play_game()
    print(data)
    return render(request, 'app/robot.html',context=data)