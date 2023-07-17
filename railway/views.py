from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse, HttpResponseNotFound
from .models import *
from .utils import *
# Create your views here.

def home(request):
    context = {
        'menu': menu,
        'title': 'Website of Ukraine Railway Station',
        }
    return render(request, 'railway/home.html', context = context)

class Schedule(DataMixin, ListView):
    model = Trains #Select all records from the table and try to display them as a list
    template_name = 'railway/schedule.html' #The path to the required html file 
    context_object_name = 'trains' #Put list records from the table in posts 

    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Train schedule'
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

class Cancelled(DataMixin, ListView):
    model = Trains #Select all records from the table and try to display them as a list
    template_name = 'railway/cancelled.html' #The path to the required html file 
    context_object_name = 'trains' #Put list records from the table in trains 

    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cancelled Trains'
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self): #Return list with elemts that meets the filter criteria
        return Trains.objects.filter(status = 'CANCELLED')

class Diverted(DataMixin, ListView):
    model = Trains #Select all records from the table and try to display them as a list
    template_name = 'railway/diverted.html' #The path to the required html file 
    context_object_name = 'trains' #Put list records from the table in trains 

    def get_context_data(self, *, object_list=None, **kwargs):  #Passing static and dynamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Diverted Trains'
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

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
        context['seats'] = Seats.objects.filter(car__train__slug = self.kwargs['train_slug'])
        context['slugs'] = self.slug_url_kwarg
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

def buy_ticket(request, train_slug, wagon_number):
    allSeats = list(Seats.objects.filter(car__train__slug = train_slug,
                                     car__number = wagon_number).values('number', 'status', 'car__train__slug', 'car__train__number'))
    
    context = {
        'title': f"Train number: {allSeats[0]['car__train__number']}",
        'seats': allSeats,
        'menu': menu,
        'wagon': wagon_number,
        'wagons': Cars.objects.filter(train__slug = train_slug).select_related('train'),
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