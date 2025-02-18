from datetime import timedelta
from django.core.mail import send_mail
from django.forms import formset_factory, modelformset_factory
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import BookingForm,PassengerForms
from .models import busdetails, Booking, Wallet,Passenger
from django.contrib import messages


def home(request):
    context = {
        'busdetails': busdetails.objects.all()
    }
    return render(request, 'exp/home.html', context)


class PostListView(ListView):
    model = busdetails
    template_name = 'exp/home.html'
    context_object_name = 'busdetails'
    ordering = ['-date_time']


class PostDetailView(ListView):
    model = busdetails


def about(request):
    return render(request, 'exp/about.html')


def search_results(request):
    from_query = request.GET.get('from', '')
    to_query = request.GET.get('to', '')
    required_buses = busdetails.objects.all()
    if from_query:
        required_buses = required_buses.filter(depart_from__icontains=from_query)
    if to_query:
        required_buses = required_buses.filter(stop1__icontains=to_query)
    return render(request, 'exp/search.html',
                  {'from_query': from_query, 'to_query': to_query, 'required_buses': required_buses})


@login_required
def book(request, bus_id):
    if not request.user.profile.email_verified:
        messages.error(request, "Please verify your email before booking a ticket.")
        return redirect('profile')
    bus = get_object_or_404(busdetails, id=bus_id)
    wallet = Wallet.objects.get(user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            no_of_seats = form.cleaned_data['no_of_seats']
            total_fare = no_of_seats * bus.fare

            if no_of_seats <= bus.availableseats and total_fare <= wallet.balance:
                booking = form.save(commit=False)
                booking.bus = bus
                booking.name = request.user
                booking.save()
                wallet.balance -= total_fare
                wallet.save()

                bus.availableseats -= no_of_seats
                bus.save()

                messages.success(request, f"Successfully booked {no_of_seats} tickets")
                send_mail(
                    subject='Confirmation mail for bus booking',
                    message=(
                        f'{booking.no_of_seats} tickets have been booked for {booking.name}. '
                        f'Date of travel:{booking.bus.date_time}.'
                        f'From {booking.bus.depart_from} To {booking.bus.stop1}.'),

                    from_email='darshpatel610@gmail.com',
                    recipient_list=[request.user.email]
                )
                return redirect('passengers',booking_id=booking.id)
            else:
                messages.error(request, "SEATS NOT AVAILABLE")
    else:
        form = BookingForm()
    return render(request, 'exp/booking_page.html', {'form': form, 'bus': bus})


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
        if booking.bus.availableseats <= booking.bus.totalseats:
            booking.bus.availableseats += booking.no_of_seats
            booking.bus.save()
        else:
            booking.bus.availableseats = booking.bus.totalseats
        total_fare = booking.no_of_seats * booking.bus.fare
        wallet.balance += total_fare
        wallet.save()

        booking.save()
        messages.success(request, "Your booking has been cancelled.")
    else:
        messages.error(request, "You cannot cancel the booking within 6 hours of departure.")
    return redirect('EXP HOME')


@login_required
def add_passenger_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, name=request.user)
    total_passengers = booking.no_of_seats
    PassengerFormSet = formset_factory(PassengerForms, extra=total_passengers)

    if request.method == 'POST':
        formset = PassengerFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                passenger = form.save(commit=False)
                passenger.booking = booking
                passenger.save()
            messages.success(request, "Passenger details added successfully.")
            return redirect('EXP HOME')
    else:
        formset = PassengerFormSet()

    return render(request, 'exp/passengers.html', {'formset': formset})

@login_required
def edit_passenger_details(request,booking_id):
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
