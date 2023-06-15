from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class StatusOfTrain(models.Model):
    normal = models.CharField(max_length=255, verbose_name= 'normal')
    cancelled = models.CharField(max_length=255, verbose_name= 'cancelled')
    diverted = models.CharField(max_length=255, verbose_name= 'diverted')

class Trains(models.Model):
    status = models.ForeignKey('StatusOfTrain', on_delete=models.PROTECT)
    from_city = models.CharField(max_length=255, verbose_name= 'from')
    to_city = models.CharField(max_length=255, verbose_name= 'to')
    departure_date = models.DateTimeField(verbose_name= 'departure_date')
    arrival_date = models.DateTimeField(verbose_name= 'arrival_date')

class Cars(models.Model):
    train = models.ForeignKey('Trains', on_delete=models.SET_NULL, null=True)
    number = models.IntegerField(verbose_name= 'Car number')

class Seats(models.Model):
    car = models.ForeignKey('Cars', on_delete=models.CASCADE, null=True)
    number = models.IntegerField(verbose_name= 'Seat number')
    status = models.BooleanField(verbose_name= 'Seat status')

class Clients(AbstractUser):
    tickets = models.ForeignKey('Seats', on_delete=models.CASCADE, null=True)