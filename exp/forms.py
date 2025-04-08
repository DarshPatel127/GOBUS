from django import forms
from .models import busdetails, Booking, Passenger, BusStop


class BookingForm(forms.ModelForm):
    #no_of_seats = forms.IntegerField(min_value=1, label="Number of Seats")

    class Meta:
        model = Booking
        fields = ['no_of_seats', 'source_stop', 'destination_stop']


class PassengerForms(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age','gender']
 
'''class BusStopForm(forms.ModelForm):
    class Meta:
        model = BusStop
        fields = ['bus','stop_name', 'stop_number', 'arrival_time', 'fare_from_start']

class BusDetailsForm(forms.ModelForm):
    class Meta:
        model = busdetails
        fields = ['bus_name', 'bus_number', 'totalseats', 'date_time', 'bus_type', 'seat_catagory', 'fare']

class BookingCreationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name','date','bus','no_of_seats', 'source_stop', 'destination_stop','is_cancelled']

class PassengerCreationForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['booking','name','age','gender']
'''
