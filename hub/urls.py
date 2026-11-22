from django.urls import path
from . import views

app_name = 'hub'

urlpatterns = [
    path('', views.home, name='home'),
    path('clubs/<int:pk>/', views.club_detail, name='club_detail'),
    path('events/', views.events, name='events'),
    path('join/', views.join, name='join'),
]