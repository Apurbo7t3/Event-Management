from django.contrib import admin
from django.urls import include, path
from organizer.views import organizer_home

urlpatterns = [
    path('organizer-home/',organizer_home,name='organizer-home'),
]
