from django.contrib import admin
from .models import *

class TrainsAdmin(admin.ModelAdmin):
    list_display = ('status', 'from_city', 'departure_date', 'arrival_date', )
    list_display_links = ('status',)
    search_fields = ('status', 'from_city', 'departure_date', 'arrival_date', )
    list_editable = ('from_city', 'departure_date', 'arrival_date', )

class CarsAdmin(admin.ModelAdmin):
    list_display = ('number', 'train')
    list_display_links = ('number', 'train')
    search_fields = ('number', 'train')
    
class SeatsAdmin(admin.ModelAdmin):
    list_display = ('car', 'number', 'user', 'status')
    list_display_links = ('car', 'number', 'status')
    search_fields = ('car', 'number', 'status')



admin.site.register(Trains, TrainsAdmin)
admin.site.register(Cars, CarsAdmin)
admin.site.register(Seats, SeatsAdmin)
