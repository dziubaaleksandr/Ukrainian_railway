from django import forms
from railway.models import *
from .widgets import *


class TrainSearchForm(forms.Form):
    from_city = forms.CharField()
    to_city = forms.CharField()
    departure_date = forms.DateTimeField(widget=DateTimePickerInput)
