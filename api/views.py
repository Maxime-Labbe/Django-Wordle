from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from app import robot

def get_data_robot(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer or not ('robot' in referer):
        return JsonResponse({'error': 'Unauthorized access'})
    
    try :
        data = robot.get_data()
    except Exception as e:
        return JsonResponse({'error': 'Unexpected error occurred'})
    return JsonResponse({'data': data})

def get_data_solo(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer or not ('solo' in referer):
        return JsonResponse({'error': 'Unauthorized access'})
    
    word = robot.get_word_to_guess()
    return JsonResponse({'data': word})