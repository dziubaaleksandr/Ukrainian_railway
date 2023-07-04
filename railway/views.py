from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.http import Http404, HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
# Create your views here.

menu = ['home', 'schedule', 'diverted', 'cancelled',]
def index(request):
    context = {
        'menu': menu,
        'title': "Home Page",
        }
    return render(request, "railway/index.html", context = context)

class Schedule(ListView):
    model = Trains #Select all records from the table and try to display them as a list
    template_name = 'railway/schedule.html' #The path to the required html file 
    context_object_name = 'trains' #Put list records from the table in posts 

    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schedule Page'
        context['menu'] = menu
        return context

    # def get_queryset(self): #Return list with elemts that meets the filter criteria
    #     return Women.objects.filter(is_published = True)

class Cancelled(ListView):
    model = Trains #Select all records from the table and try to display them as a list
    template_name = 'railway/cancelled.html' #The path to the required html file 
    context_object_name = 'trains' #Put list records from the table in posts 

    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cancelled Trains Page'
        context['menu'] = menu
        return context

    def get_queryset(self): #Return list with elemts that meets the filter criteria
        return Trains.objects.filter(status = 'CANCELLED')

class Diverted(ListView):
    model = Trains #Select all records from the table and try to display them as a list
    template_name = 'railway/diverted.html' #The path to the required html file 
    context_object_name = 'trains' #Put list records from the table in posts 

    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cancelled Trains Page'
        context['menu'] = menu
        return context

    def get_queryset(self): #Return list with elemts that meets the filter criteria
        return Trains.objects.filter(status = 'DIV')
    
class ShowTrain(DetailView):
    model = Trains
    template_name = "railway/train.html"
    context_object_name = 'trains'
    slug_url_kwarg = "train_slug" #specify the name of slug
    
    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = f"Train number: {context['trains'].number}"
        context['menu'] = menu
        context['seats'] = Seats.objects.filter(car__train__slug = self.kwargs['train_slug'])
        context['slugs'] = self.slug_url_kwarg
        return context
    
def buy_ticket(request, train_slug, wagon_number):
    #trains = Trains.objects.filter(slug = train_slug).values('number')
    allSeats = Seats.objects.filter(car__train__slug = train_slug,
                                     car__number = wagon_number).select_related('car').values('number', 'status', 'car__train__slug', 'car__train__number')
    context = {
        #'title': f"Train number: {trains[0]['number']}",
        'title': f"Train number: {allSeats[0]['car__train__number']}",
        'seats': Seats.objects.filter(car__train__slug = train_slug, car__number = wagon_number).select_related('car').values('number', 'status', 'car__train__slug'),
        'menu': menu,
        'wagon': wagon_number,
        'numberOfWagons': range(1, Cars.objects.filter(train__slug = train_slug).select_related('train').count() + 1),
        }
    
    if request.method == 'POST':
        seats = Seats.objects.filter(car__train__slug = train_slug, car__number = wagon_number)
        for seat in seats:
            if request.user.is_authenticated and request.POST.get(str(seat.number)):
                s1 = Seats.objects.filter(car__train__slug = train_slug, car__number = wagon_number, number = seat.number).select_related('car')
                s1.update(user_id = request.user.id, status = 'BOUGHT')
            else:
                break
        
        seats = Seats.objects.filter(car__train__slug = train_slug, car__number = wagon_number).select_related('car').values('number', 'status', 'car__train__slug')
        context['seats'] = seats
        
    return render(request, "railway/train.html", context= context)
    
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'railway/register.html'
    success_url = reverse_lazy('home')
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        context['menu'] = menu
        return context
    
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'railway/login.html'
 
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