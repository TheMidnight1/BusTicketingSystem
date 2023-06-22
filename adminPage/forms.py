# forms.py
from django import forms
from django.forms import DateInput
from django.forms import FileInput
from Bus.models import Bus,Seat

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'
        widgets = {
            'travel_dates': DateInput(attrs={'type': 'date'}),
            'image': FileInput(attrs={'type': 'file' }),
        }


class SeatForm(forms.Form):
    selected_seats = forms.CharField(widget=forms.HiddenInput())
