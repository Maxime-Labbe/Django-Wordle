from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import robot

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def solo(request):
    return render(request, 'app/solo.html')

def robot_view(request):
    data = robot.get_data()
    return render(request, 'app/robot.html',context=data)

def get_data(request):
    data = robot.get_data()
    return JsonResponse({'data': data})