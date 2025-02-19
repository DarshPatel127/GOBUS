from django.contrib import admin
from .models import busdetails, Booking, Wallet, Passenger, BusStop

admin.site.register(busdetails)
admin.site.register(Booking)
admin.site.register(Wallet)
admin.site.register(Passenger)
admin.site.register(BusStop)
