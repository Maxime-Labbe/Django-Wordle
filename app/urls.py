from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('solo/', views.solo, name='solo'),
    path('robot/', views.robot_view, name='robot'),
]