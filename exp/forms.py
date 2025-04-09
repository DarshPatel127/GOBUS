from django import forms
from .models import busdetails, Booking, Passenger, BusStop


class BookingForm(forms.ModelForm):
    #no_of_seats = forms.IntegerField(min_value=1, label="Number of Seats")

    class Meta:
        model = Booking
        fields = ['no_of_seats', 'source_stop', 'destination_stop']

    def __init__(self, *args, bus=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.bus = bus
        if bus:
            self.fields['source_stop'].queryset = bus.stops.all()
            self.fields['destination_stop'].queryset = bus.stops.all()


class PassengerForms(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age','gender']
 
