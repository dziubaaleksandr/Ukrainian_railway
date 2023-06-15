from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound
# Create your views here.

def index(request):
    return HttpResponse("<h1>Page not Found</h1>")

