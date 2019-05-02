from django.urls import path
from . import views
urlpatterns = [
    path('request/', views.request, name='request'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views._login, name='login'),
    path('logout/', views._logout, name='logout'),
]