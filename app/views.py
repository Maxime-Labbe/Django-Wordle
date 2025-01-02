from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from . import robot
import requests

def index(request):
    return render(request, 'app/index.html')

def solo(request):
    return render(request, 'app/solo.html')

def robot_view(request):
    robot.set_data(robot.play_game())
    data = robot.get_data()
    return render(request, 'app/robot.html',context=data)