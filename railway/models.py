from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin

class Trains(models.Model):
    number = models.IntegerField("TrainNumber")
    status = models.CharField('StatusOfTrain', max_length=9, choices=(('NORM', 'normal'), ('CANCELLED', 'cancelled'), ('DIV', 'diverted')), default='normal')
    from_city = models.CharField(max_length=255, verbose_name= 'from')
    to_city = models.CharField(max_length=255, verbose_name= 'to')
    departure_date = models.DateTimeField(verbose_name= 'departure_date')
    arrival_date = models.DateTimeField(verbose_name= 'arrival_date')
    slug = models.SlugField(max_length=255, unique=False, db_index = True, verbose_name="URL")

    def __str__(self):
        return f"Number {self.number} from {self.from_city} to {self.to_city}"
    
    def get_absolute_url(self):
        return reverse('train', kwargs = {'train_slug': self.slug, 'wagon_number': 1})
    
class Cars(models.Model):
    train = models.ForeignKey('Trains', on_delete=models.SET_NULL, null=True)
    number = models.IntegerField(verbose_name= 'Car number')
    def __str__(self):
        return f"Train {self.train} Car number {self.number}"

class Seats(models.Model):
    car = models.ForeignKey('Cars', on_delete=models.CASCADE, null=True)
    number = models.IntegerField(verbose_name= 'Seat number')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank = True)
    status = models.CharField('SeatStatus', max_length=6, choices=(('FREE', 'free'), ('BOUGHT', 'bought')), default="FREE")
    def __str__(self):
        return f"Car number {self.car} Seat number {self.number}"

    def save(self, *args, **kwargs):
        if self.user:
            print(f"Model {self.user}")
            self.status = 'BOUGHT' 
            print(f"Model {self.status}")
        else:
            print(f"Model {self.user}")
            self.status = 'FREE'
            print(f"Model {self.status}")
        super().save(*args, **kwargs)
        


    
    

