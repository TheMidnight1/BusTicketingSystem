from django import forms
from django.utils import timezone


class SearchForm(forms.Form):
    source = forms.CharField(
        label="Source",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Source'}),
        error_messages={
            'required': 'Please enter the source.',
        }
    )
    destination = forms.CharField(
        label="Destination",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Destination'}),
        error_messages={
            'required': 'Please enter the destination.',
        }
    )
    travel_date = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={
            'required': 'Please select a travel date.',
            'invalid': 'Please enter a valid date.',
        }
    )

    def clean_travel_date(self):
        travel_date = self.cleaned_data['travel_date']
        if travel_date < timezone.now().date():
            raise forms.ValidationError("Travel date cannot be in the past.")
        return travel_date
