from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import BookingForm
from .models import busdetails, Booking, Wallet
from django.contrib import messages
from django.urls import reverse


def home(request):
    context = {
        'busdetails': busdetails.objects.all()
    }
    return render(request, 'exp/home.html', context)


class PostListView(ListView):
    model = busdetails
    template_name = 'exp/home.html'
    context_object_name = 'busdetails'
    # ordering = ['-date']


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

                messages.success(request, f"Successfully booked {no_of_seats} ticket")
                return redirect('EXP HOME')
            else:
                messages.error(request, "SEATS NOT AVAILABLE")
    else:
        form = BookingForm()
    return render(request, 'exp/booking_page.html', {'form': form, 'bus': bus})
