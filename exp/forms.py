from django import forms
from .models import busdetails, Booking, Passenger, BusStop


class BookingForm(forms.ModelForm):
    #no_of_seats = forms.IntegerField(min_value=1, label="Number of Seats")

    class Meta:
        model = Booking
        fields = ['no_of_seats', 'source_stop', 'destination_stop']

    def __init__(self, *args, **kwargs):
        bus = kwargs.pop('bus', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        if bus:
            self.fields['source_stop'].queryset = BusStop.objects.filter(bus=bus).order_by('stop_number')
            self.fields['destination_stop'].queryset = BusStop.objects.filter(bus=bus).order_by('stop_number')



class PassengerForms(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age','gender']
