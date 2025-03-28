from django.contrib import admin
from .models import busdetails, Booking, Wallet, Passenger, BusStop,RunningDay
class Busadmin(admin.ModelAdmin):
    list_display = ['bus_name', 'busadmin']
    readonly_fields = ['busadmin']
    
    def get_queryset(self, request):
        data = super().get_queryset(request)
        if request.user.is_superuser:
            return data
        return data.filter(busadmin=request.user)
    
    def save_model(self, request, obj, form, change):
        obj.busadmin = request.user
        obj.save()

class BusStopadmin(admin.ModelAdmin):
    list_display = list_display = ['bus', 'stop_name', 'stop_number']

    def get_queryset(self, request):
        data = super().get_queryset(request)
        if request.user.is_superuser:
            return data
        return data.filter(bus__busadmin=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.bus.busadmin:
            obj.bus.busadmin = request.user
            obj.bus.save()
        obj.save()

class Bookingadmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'no_of_seats', 'bus', 'source_stop', 'destination_stop', 'is_cancelled']

    def get_queryset(self, request):
        data = super().get_queryset(request)
        if request.user.is_superuser:
            return data
        return data.filter(bus__busadmin=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.bus.busadmin:
            obj.bus.busadmin = request.user
            obj.bus.save()
        obj.save()

class Passengeradmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender']

    def get_queryset(self, request):
        data = super().get_queryset(request)
        if request.user.is_superuser:
            return data
        return data.filter(booking__bus__busadmin=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.booking.bus.busadmin:
            obj.booking.bus.busadmin = request.user
            obj.booking.bus.save()
        obj.save()

admin.site.register(busdetails, Busadmin)
admin.site.register(Booking, Bookingadmin)
admin.site.register(Passenger, Passengeradmin)
admin.site.register(BusStop, BusStopadmin)
admin.site.register(Wallet)
admin.site.register(RunningDay)
