from django.urls import path
from . import views

app_name = 'hub'

urlpatterns = [
    path('', views.home, name='home'),
    path('clubs/<int:pk>/', views.club_detail, name='club_detail'),
    path('events/', views.events, name='events'),
    path('join/', views.join, name='join'),
    path('requests/<int:pk>/approve/', views.approve_request, name='approve_request'),
    path('requests/<int:pk>/reject/', views.reject_request, name='reject_request'),

]