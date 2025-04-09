from django.contrib import admin
from .models import busdetails, Booking, Wallet, Passenger, BusStop, RunningDay


# Register models with default admin site
admin.site.register(busdetails)
admin.site.register(Booking)
admin.site.register(Passenger)
admin.site.register(BusStop)
admin.site.register(Wallet)
admin.site.register(RunningDay)