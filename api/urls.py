from django.urls import path
from api import views

urlpatterns = [
    path('get_data/', views.get_data, name='get_data'),
    path('get_word_to_guess/', views.get_word_to_guess, name='get_word_to_guess'),
]