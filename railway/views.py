from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound
# Create your views here.

def index(request):
    return render(request, 'railway/index.html', {'title': "Main"})

