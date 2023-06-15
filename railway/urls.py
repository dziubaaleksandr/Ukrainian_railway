from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = "home"),
    path('schedule/', schedule, name = "schedule"),
    path('diverted/', diverted, name = "diverted"),
    path('cancelled/', cancelled, name = "cancelled"),
   
]
