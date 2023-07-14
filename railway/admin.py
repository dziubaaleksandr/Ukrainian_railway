from django.contrib import admin
from .models import *

class TrainsAdmin(admin.ModelAdmin):
    list_display = ('number', 'status', 'from_city', 'to_city', 'departure_date', 'arrival_date', )
    list_display_links = ('number',)
    search_fields = ('status', 'from_city', 'to_city', 'departure_date', 'arrival_date', )
    list_editable = ('status', 'from_city', 'to_city', 'departure_date', 'arrival_date', )
    prepopulated_fields = {'slug': ('from_city', 'to_city' )}

class CarsAdmin(admin.ModelAdmin):
    list_display = ('number', 'train')
    list_display_links = ('number', 'train')
    search_fields = ('number', 'train__slug')
    
class SeatsAdmin(admin.ModelAdmin):
    list_display = ('car', 'number', 'user', 'status')
    list_display_links = ('car', 'number',)
    list_editable = ('user', 'status', )
    search_fields = ('car__number', 'car__train__from_city', 'car__train__to_city', 'number', 'status')

admin.site.register(Trains, TrainsAdmin)
admin.site.register(Cars, CarsAdmin)
admin.site.register(Seats, SeatsAdmin)
