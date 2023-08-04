from django import forms
from railway.models import *


class TrainSearchForm(forms.Form):
    from_city = forms.CharField()
    to_city = forms.CharField()
    
