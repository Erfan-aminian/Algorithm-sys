from . import views
from django.urls import path, include
app_name = 'home'
urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('count/', views.GetProcessCountView.as_view(), name='count'),
    path('dynamic/', views.DynamicProcessView.as_view(), name='dynamic'),
    path('fcfs/', views.Fcfsview.as_view(), name='fcfs'),
    path('roundrobin/', views.RoundRobinView.as_view(), name='rr'),
    path('sjf/', views.SjfView.as_view(), name='sjf'),
    path('srt/', views.SrtView.as_view(), name='srt'),


]