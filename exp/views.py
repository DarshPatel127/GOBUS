from datetime import timedelta
from django.core.mail import send_mail
from django.forms import formset_factory, modelformset_factory
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db import transaction
from django.contrib import messages

from . import models
from .forms import BookingForm, PassengerForms
from .models import busdetails, Booking, Wallet, Passenger, BusStop
from django.contrib import messages
from django.db.models import Q


def home(request):
    context = {
        'busdetails': busdetails.objects.prefetch_related('stops').all().filter(date_time__gte=timezone.now()),
    }
    return render(request, 'exp/home.html', context)


def search_results(request):
    from_query = request.GET.get('from', '')
    to_query = request.GET.get('to', '')
    date = request.GET.get('date')
    sort_by = request.GET.get('sort', 'date_time')

    available_buses = {}

    if from_query and to_query:
        buses = busdetails.objects.prefetch_related('stops').all().filter(date_time__gte=timezone.now())

        for bus in buses:
            stops = bus.stops.all()
            source_stop = stops.filter(stop_name__icontains = from_query).first()
            destination_stop = stops.filter(stop_name__icontains=to_query).first()



            if source_stop and destination_stop and source_stop.stop_number < destination_stop.stop_number:
                occupied_seats = get_occupied_seats(
                    bus,
                    source_stop.stop_number,
                    destination_stop.stop_number
                )
                available_seats = bus.totalseats - occupied_seats

                if available_seats > 0:
                    available_buses[bus.id] = {
                        'bus_name': bus.bus_name,
                        'bus_number': bus.bus_number,
                        'source_stop': source_stop.stop_name,
                        'destination_stop': destination_stop.stop_name,
                        'souce_stop_id': source_stop.id,
                        'destination_stop_id': destination_stop.id,
                        'available_seats': available_seats,
                        'source_arrival_time':source_stop.arrival_time,
                        'destination_arrival_time': destination_stop.arrival_time,
                        'fare': destination_stop.fare_from_start - source_stop.fare_from_start
                    }

        available_buses = dict(sorted(available_buses.items(), key=lambda x: x[1]['source_stop'], reverse=True))
    return render(request, 'exp/search.html',{'from_query': from_query, 'to_query': to_query, 'available_buses':available_buses})

def get_occupied_seats(bus, start_stop, end_stop):
    overlapping_bookings = Booking.objects.filter(
        bus = bus,
        is_cancelled =False
    ).filter(
        (
            Q(source_stop__stop_number__lt=end_stop) &
            Q(destination_stop__stop_number__gt=start_stop)
        )
    )

    return  sum(booking.no_of_seats for booking in overlapping_bookings)


@login_required
def book(request, bus_id):
    if not request.user.profile.email_verified:
        messages.error(request, "Please verify your email before booking a ticket.")
        return redirect('profile')

    bus = get_object_or_404(busdetails, id=bus_id)
    stops = BusStop.objects.filter(bus=bus).order_by('stop_number')

    PassengerFormSet = formset_factory(PassengerForms, extra=0)
    formset = PassengerFormSet()

    if request.method == 'GET':
        source_stop_id = request.GET.get('source_stop')
        destination_stop_id = request.GET.get('destination_stop')
        initial_data = {}
        if source_stop_id:
            initial_data['source_stop'] = source_stop_id
        if destination_stop_id:
            initial_data['destination_stop'] = destination_stop_id
        form = BookingForm(bus=bus, initial=initial_data or None)
        formset= PassengerFormSet()
    elif request.method == 'POST':
        form = BookingForm(request.POST, bus=bus)
        no_of_seats = int(request.POST.get('no_of_seats', 0))
        PassengerFormSet = modelformset_factory(Passenger, form=PassengerForms, extra=no_of_seats)
        formset = PassengerFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            source_stop_id = request.POST.get('source_stop')
            destination_stop_id = request.POST.get('destination_stop')

            try:
                source_stop = stops.get(id=source_stop_id)
                destination_stop = stops.get(id=destination_stop_id)

                if source_stop.stop_number >= destination_stop.stop_number:
                    messages.error(request, "Invalid stop selection")
                    return render(request, 'exp/booking_page.html', {'booking_form': form,'passenger_formset':formset, 'bus': bus, 'stops': stops})

                no_of_seats = form.cleaned_data['no_of_seats']
                fare = destination_stop.fare_from_start - source_stop.fare_from_start
                total_fare = no_of_seats * fare

                wallet = Wallet.objects.get(user=request.user)

                # Check seat availability
                occupied_seats = get_occupied_seats(bus, source_stop.stop_number, destination_stop.stop_number)
                available_seats = bus.totalseats - occupied_seats

                if no_of_seats <= available_seats and total_fare <= wallet.balance:
                    with transaction.atomic():

                        booking = form.save(commit=False)
                        booking.bus = bus
                        booking.name = request.user
                        booking.source_stop = source_stop
                        booking.destination_stop = destination_stop
                        booking.save()

                        wallet.balance -= total_fare
                        wallet.save()
                        for passenger_form in formset:
                            passenger = passenger_form.save(commit=False)
                            passenger.booking = booking
                            passenger.save()



                    messages.success(request, f"Successfully booked {no_of_seats} tickets")
                    return redirect('EXP HOME')
                else:
                    messages.error(request, "Insufficient seats or wallet balance")

            except BusStop.DoesNotExist:
                messages.error(request, "Invalid stop selection")

        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, 'exp/booking_page.html', {
        'booking_form': form,
        'bus': bus,
        'stops': stops,
        'passenger_formset': formset
    })


@login_required
def booking_panel(request):
    booked_tickets = Booking.objects.filter(name=request.user).select_related('bus').order_by('-date')

    context = {'booked_tickets': booked_tickets}
    return render(request, 'exp/view_bookings.html', context)


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, name=request.user)
    context = {'bookings': Booking.objects.filter(name=request.user)}
    wallet = Wallet.objects.get(user=request.user)
    if booking.bus.date_time >= (timedelta(hours=6) + timezone.now()):
        booking.is_cancelled = True
        fare = booking.destination_stop.fare_from_start - booking.source_stop.fare_from_start
        total_fare = booking.no_of_seats * fare
        wallet.balance += total_fare
        wallet.save()

        booking.save()
        messages.success(request, "Your booking has been cancelled.")
    else:
        messages.error(request, "You cannot cancel the booking within 6 hours of departure.")
    return redirect('EXP HOME')





@login_required
def edit_passenger_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, name=request.user)
    PassengerFormSet = modelformset_factory(Passenger, form=PassengerForms, extra=0)
    queryset = booking.passengers.all()

    if request.method == 'POST':
        formset = PassengerFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Passenger details updated successfully.")
            return redirect('EXP HOME')  # Adjust as needed
    else:
        formset = PassengerFormSet(queryset=queryset)

    return render(request, 'exp/edit_passengers.html', {'formset': formset})
