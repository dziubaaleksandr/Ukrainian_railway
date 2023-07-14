from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name = 'register'),
    path('login/', LoginUser.as_view(), name = 'login'),
    path('logout/', logout_user, name='logout'),
    path('account/', account , name = 'account'),
    path('my_tickets/', UsersTicket.as_view(), name = 'print_tickets'),
    path('account/change_password/', ChangePassword.as_view() , name = 'change_password'),
]