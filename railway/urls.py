from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = "home"),
    path('schedule/', Schedule.as_view(), name = "schedule"),
    path('diverted/', Diverted.as_view(), name = "diverted"),
    path('cancelled/', Cancelled.as_view(), name = "cancelled"),
   
]
