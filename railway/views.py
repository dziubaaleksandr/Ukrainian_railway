from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound
# Create your views here.

def index(request):
    return render(request, 'railway/index.html', {'title': "Main"})

def schedule(request):
    return render(request, 'railway/schedule.html', {'title': "Main"})

def diverted(request):
    return render(request, 'railway/diverted.html', {'title': "Main"})

def cancelled(request):
    return render(request, 'railway/cancelled.html', {'title': "Main"})

