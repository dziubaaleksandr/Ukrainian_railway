from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound
# Create your views here.

menu = ['home', 'schedule', 'diverted', 'cancelled']
def index(request):
    context = {
        'menu': menu,
        'title': "Home Page",
        }
    return render(request, "railway/index.html", context = context)

def schedule(request):
    return render(request, 'railway/schedule.html', {'title': "Schedule", 'menu': menu})

def diverted(request):
    return render(request, 'railway/diverted.html', {'title': "Main"})

def cancelled(request):
    return render(request, 'railway/cancelled.html', {'title': "Main"})

