from django import forms
from .models import busdetails, Booking


class BookingForm(forms.ModelForm):
    no_of_seats = forms.IntegerField(min_value=1, label="Number of Seats")
    class Meta:
        model = Booking
        fields = ['no_of_seats']
