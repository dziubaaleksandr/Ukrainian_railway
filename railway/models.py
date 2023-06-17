from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class Trains(models.Model):
    status = models.CharField('StatusOfTrain', max_length=9, choices=(('NORM', 'normal'), ('CANCELLED', 'cancelled'), ('DIV', 'diverted')), default='normal')
    from_city = models.CharField(max_length=255, verbose_name= 'from')
    to_city = models.CharField(max_length=255, verbose_name= 'to')
    departure_date = models.DateTimeField(verbose_name= 'departure_date')
    arrival_date = models.DateTimeField(verbose_name= 'arrival_date')

    def __str__(self):
        return f"{self.from_city} {self.to_city}"
    
class Cars(models.Model):
    train = models.ForeignKey('Trains', on_delete=models.SET_NULL, null=True)
    number = models.IntegerField(verbose_name= 'Car number')
    def __str__(self):
        return f"{self.train} {self.number}"

class Seats(models.Model):
    car = models.ForeignKey('Cars', on_delete=models.CASCADE, null=True)
    number = models.IntegerField(verbose_name= 'Seat number')
    status = models.BooleanField(verbose_name= 'Seat status')
    def __str__(self):
        return f"{self.car} {self.number}"

class Clients(AbstractUser):
    tickets = models.ForeignKey('Seats', on_delete=models.CASCADE, null=True)