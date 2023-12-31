from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse, HttpResponseNotFound
from datetime import datetime
from .models import *
from .utils import *
from .forms import *
# Create your views here.


def home(request):
    context = {
        'menu': menu,
        'title': 'Website of Ukraine Railway Station',
    }
    return render(request, 'railway/home.html', context=context)


class RailwayHome(DataMixin, ListView):
    model = Trains
    template_name = 'railway/home.html'
    context_object_name = 'trains'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = TrainSearchForm()
        if self.request.GET:
            context['form'] = TrainSearchForm(self.request.GET)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Return list with elemts that meets the filter criteria
        if self.request.GET.get('from_city') and self.request.GET.get('to_city'):
            from_city = self.request.GET.get('from_city')
            to_city = self.request.GET.get('to_city')
            departure_date = self.request.GET.get('departure_date')
            return Trains.objects.filter(from_city=from_city,
                                         to_city=to_city, departure_date__date=datetime.strptime(
                                             departure_date, '%Y-%m-%dT%H:%M').date(),
                                         departure_date__time__gte=datetime.strptime(departure_date, '%Y-%m-%dT%H:%M').time()) if Trains.objects.filter(from_city=from_city, to_city=to_city, departure_date__date=datetime.strptime(departure_date, '%Y-%m-%dT%H:%M').date(), departure_date__time__gte=datetime.strptime(departure_date, '%Y-%m-%dT%H:%M').time()) else None
        return []


class Schedule(DataMixin, ListView):
    model = Trains  # Select all records from the table and try to display them as a list
    template_name = 'railway/schedule.html'  # The path to the required html file
    context_object_name = 'trains'  # Put list records from the table in posts

    # Passing static and dynamic data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Train schedule'
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class Cancelled(DataMixin, ListView):
    model = Trains  # Select all records from the table and try to display them as a list
    template_name = 'railway/cancelled.html'  # The path to the required html file
    context_object_name = 'trains'  # Put list records from the table in trains

    # Passing static and dynamic data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cancelled Trains'
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Return list with elemts that meets the filter criteria
        return Trains.objects.filter(status='CANCELLED')


class Diverted(DataMixin, ListView):
    model = Trains  # Select all records from the table and try to display them as a list
    template_name = 'railway/diverted.html'  # The path to the required html file
    context_object_name = 'trains'  # Put list records from the table in trains

    # Passing static and dynamic data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Diverted Trains'
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Return list with elemts that meets the filter criteria
        return Trains.objects.filter(status='DIV')


class ShowTrain(DetailView):
    model = Trains
    template_name = 'railway/train.html'
    context_object_name = 'trains'
    slug_url_kwarg = 'train_slug'  # specify the name of slug

    # Passing static and dynamic data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Train number: {context['trains'].number}"
        context['seats'] = Seats.objects.filter(
            car__train__slug=self.kwargs['train_slug'])
        context['slugs'] = self.slug_url_kwarg
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


def buy_ticket(request, train_slug, wagon_number):
    allSeats = list(Seats.objects.filter(car__train__slug=train_slug,
                                         car__number=wagon_number).values('number', 'status', 'car__train__slug', 'car__train__number', 'car__train__status'))

    context = {
        'title': f"Train number: {allSeats[0]['car__train__number']}",
        'seats': allSeats,
        'menu': menu,
        'wagon': wagon_number,
        'wagons': Cars.objects.filter(train__slug=train_slug).select_related('train'),
    }

    if request.method == 'POST':
        for seat in allSeats:
            if request.user.is_authenticated:
                if request.POST.get(str(seat['number'])):
                    s1 = Seats.objects.filter(car__train__slug=train_slug, car__number=wagon_number,
                                              number=seat['number']).select_related('car__train', 'car')
                    s1.update(user_id=request.user.id, status='BOUGHT')
            else:
                break

        seats = Seats.objects.filter(car__train__slug=train_slug, car__number=wagon_number).values(
            'number', 'status', 'car__train__slug', 'car__train__status')
        context['seats'] = seats

    return render(request, 'railway/train.html', context=context)
