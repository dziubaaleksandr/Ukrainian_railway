from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout
from railway.models import *
from django.contrib.auth.forms import AuthenticationForm, AdminPasswordChangeForm
from .forms import *
# Create your views here.
menu = ['home', 'schedule', 'diverted', 'cancelled',]

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        context['menu'] = menu
        return context
    
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'account/login.html'
 
    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        context['menu'] = menu
        return context

    def get_success_url(self):
        return reverse_lazy('home')
    
def logout_user(request):
    logout(request)
    return redirect('login')

def account(request):
    context = {
        'menu': menu,
        'title': 'Account',
        'user': request.user,
        }
    return render(request, 'account/account.html', context = context)

class UsersTicket(ListView):
    model = Seats 
    template_name = 'account/users_tickets.html' 
    context_object_name = 'tickets' 

    def get_context_data(self, *, object_list=None, **kwargs):  
        context = super().get_context_data(**kwargs)
        context['title'] = 'My tickets'
        context['menu'] = menu
        return context

    def get_queryset(self): 
        return Seats.objects.filter(user = self.request.user).values(
                                                                    'number', 'car__train__from_city','car__train__to_city',
                                                                    'car__train__slug', 'car__train__departure_date', 'car__train__arrival_date',
                                                                    'car__number')
    
class ChangePassword(SuccessMessageMixin, PasswordChangeView):
    form_class = AdminPasswordChangeForm
    template_name = 'account/change_password.html'
    success_message = 'Password has changed!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        context['menu'] = menu
        return context

    def get_success_url(self):
        return reverse_lazy('account')
    
def change_password(request): #NOT USED. JUST FOR EXAMPLE
    context = {
        'menu': menu,
        'title': 'Change password',
        'user': request.user,
        }

    if request.method == 'POST': 
        form = AdminPasswordChangeForm(request.user, request.POST)
        context['form'] = form
        if form.is_valid():
            request.user.set_password(request.POST.get('password1'))
            request.user.save() 
            return redirect('login')
    else:
        context['form'] = AdminPasswordChangeForm(request.user)

    return render(request, 'railway/change_password.html', context=context)