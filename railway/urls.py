from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = "home"),
    path('schedule/', Schedule.as_view(), name = "schedule"),
    path('diverted/', Diverted.as_view(), name = "diverted"),
    path('cancelled/', Cancelled.as_view(), name = "cancelled"),
    #path('schedule/<slug:train_slug>/', ShowTrain.as_view(), name = 'train')
    path('schedule/<slug:train_slug>/<int:wagon_number>/', buy_ticket, name = 'train'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('account/', account , name = 'account'),
    # path('account/change_password/', change_password , name = 'change_password'),
    path('account/change_password/', ChangePassword.as_view() , name = 'change_password'),

   
]
