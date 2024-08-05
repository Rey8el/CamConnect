from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.lobby),
    path('room/', views.room),
    path('getToken/', views.getToken),
    path('create_member/',views.createMember),
    path('get_member/',views.get_member),
    path('delete_member/',views.deleteMember),
]
