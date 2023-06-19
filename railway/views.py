from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.http import Http404, HttpResponse, HttpResponseNotFound
from .models import *
# Create your views here.

menu = ['home', 'schedule', 'diverted', 'cancelled']
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