from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from app import robot

def get_data(request):
    secret_token = request.headers.get('X-SECRET-TOKEN')
    if secret_token != settings.SECRET_API_TOKEN:
        return JsonResponse({'error': 'Unauthorized access'}, status=401)
    referer = request.META.get('HTTP_REFERER')
    if not referer or not ('robot' in referer):
        return JsonResponse({'error': 'Unauthorized access'})
    
    try :
        data = robot.get_data()
    except Exception as e:
        return JsonResponse({'error': 'Unexpected error occurred'})
    return JsonResponse({'data': data})

def get_word_to_guess(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer or not ('solo' in referer):
        return JsonResponse({'error': 'Unauthorized access'})
    
    word = robot.get_word_to_guess()
    return JsonResponse({'word_to_guess': word})