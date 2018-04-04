from django import forms
from fiesta.models import EVENT_TYPES, PARISH, EVENT_COST_RANGE

class SearchForm(forms.Form):
    title = forms.CharField(max_length=250) 


#class FilterForm(forms.Form):
    #event_type = forms.CharField(max_length=5, choices=EVENT_TYPES)
    #cost_range = forms.IntegerField(choices=EVENT_COST_RANGE) 
    #parish = forms.CharField(max_length=5, choices=PARISH)

