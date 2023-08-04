from django.urls import path
from .views import *

urlpatterns = [
    path('', RailwayHome.as_view(), name="home"),
    path('schedule/', Schedule.as_view(), name="schedule"),
    path('diverted/', Diverted.as_view(), name="diverted"),
    path('cancelled/', Cancelled.as_view(), name="cancelled"),
    path('schedule/<slug:train_slug>/<int:wagon_number>/',
         buy_ticket, name='train'),
]
