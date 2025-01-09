from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from . import robot

def index(request):
    return render(request, 'app/index.html')

def solo(request):
    robot.set_word_to_guess()
    data = robot.get_word_to_guess()
    return render(request, 'app/solo.html',context=data)

def robot_view(request):
    robot.set_data(robot.play_game())
    data = robot.get_data()
    return render(request, 'app/robot.html',context=data)