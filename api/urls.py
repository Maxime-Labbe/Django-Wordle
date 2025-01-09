from django.urls import path
from api import views

urlpatterns = [
    path('get_data_robot/', views.get_data_robot, name='get_data_robot'),
    path('get_data_solo/', views.get_data_solo, name='get_data_solo'),
]