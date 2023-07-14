from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse, HttpResponseNotFound
from .models import *

# Create your views here.

menu = ['home', 'schedule', 'diverted', 'cancelled',]

def home(request):
    context = {
        'menu': menu,
        'title': 'Website of Ukraine Railway Station',
        }
    return render(request, 'railway/home.html', context = context)

class Schedule(ListView):
    model = Trains #Select all records from the table and try to display them as a list
    template_name = 'railway/schedule.html' #The path to the required html file 
    context_object_name = 'trains' #Put list records from the table in posts 

    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Train schedule'
        context['menu'] = menu
        return context

class Cancelled(ListView):
    model = Trains #Select all records from the table and try to display them as a list
    template_name = 'railway/cancelled.html' #The path to the required html file 
    context_object_name = 'trains' #Put list records from the table in trains 

    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cancelled Trains'
        context['menu'] = menu
        return context

    def get_queryset(self): #Return list with elemts that meets the filter criteria
        return Trains.objects.filter(status = 'CANCELLED')

class Diverted(ListView):
    model = Trains #Select all records from the table and try to display them as a list
    template_name = 'railway/diverted.html' #The path to the required html file 
    context_object_name = 'trains' #Put list records from the table in trains 

    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Diverted Trains'
        context['menu'] = menu
        return context

    def get_queryset(self): #Return list with elemts that meets the filter criteria
        return Trains.objects.filter(status = 'DIV')
    
class ShowTrain(DetailView):
    model = Trains
    template_name = 'railway/train.html'
    context_object_name = 'trains'
    slug_url_kwarg = 'train_slug' #specify the name of slug
    
    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = f"Train number: {context['trains'].number}"
        context['menu'] = menu
        context['seats'] = Seats.objects.filter(car__train__slug = self.kwargs['train_slug'])
        context['slugs'] = self.slug_url_kwarg
        return context

def buy_ticket(request, train_slug, wagon_number):
    allSeats = list(Seats.objects.filter(car__train__slug = train_slug,
                                     car__number = wagon_number).values('number', 'status', 'car__train__slug', 'car__train__number'))
    context = {
        'title': f"Train number: {allSeats[0]['car__train__number']}",
        'seats': allSeats,
        'menu': menu,
        'wagon': wagon_number,
        'numberOfWagons': range(1, Cars.objects.filter(train__slug = train_slug).select_related('train').count() + 1),
        }
    
    if request.method == 'POST':
        for seat in allSeats:
            if request.user.is_authenticated:
                if request.POST.get(str(seat['number'])):
                    s1 = Seats.objects.filter(car__train__slug = train_slug, car__number = wagon_number, number = seat['number']).select_related('car__train', 'car')
                    s1.update(user_id = request.user.id, status = 'BOUGHT')
            else:
                break
        
        seats = Seats.objects.filter(car__train__slug = train_slug, car__number = wagon_number).values('number', 'status', 'car__train__slug')
        context['seats'] = seats
        
    return render(request, 'railway/train.html', context = context)