from django.contrib.auth.models import User
import datetime
from django.db import models
from datetime import datetime

class RunningDay(models.Model):
    Days=[
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        ('Sunday','Sunday'),
    ]
    day = models.CharField( choices=Days)
    def __str__(self):
        return self.day

class busdetails(models.Model):
    Seat_Categories = (
        ('GEN', 'general'),
        ('SLP', 'sleeper'),
        ('LXY', 'luxury'),
    )
    bus_name = models.CharField(max_length=50)
    bus_number = models.CharField(max_length=10)
    date_time = models.DateTimeField(default=datetime.now())
    totalseats = models.PositiveIntegerField()
    fare = models.PositiveIntegerField()
    seat_category = models.CharField(max_length=3, choices=Seat_Categories,default='GEN')
    busadmin = models.ForeignKey(User, on_delete=models.CASCADE)
    running_days = models.ManyToManyField('RunningDay')

    def __str__(self):
        return self.bus_name

    def delete(self, *args, **kwargs):
        bookings = Booking.objects.filter(bus=self, is_cancelled=False)
        for booking in bookings:
            wallet = Wallet.objects.get(user=booking.name)
            total_fare = booking.no_of_seats * self.fare
            wallet.balance += total_fare
            wallet.save()
            booking.is_cancelled = True
            booking.save()
        super(busdetails, self).delete(*args, **kwargs)



class BusStop(models.Model):
    bus = models.ForeignKey(busdetails, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=50)
    stop_number = models.PositiveIntegerField()  # the main order of the stops
    arrival_time = models.DateTimeField()
    fare_from_start = models.PositiveIntegerField()  # cummulative fare instead of indivisual fare ig

    class Meta:
        ordering = ['stop_number']
        unique_together = ['bus', 'stop_number']

    def __str__(self):
        return f"{self.bus.bus_name} - Stop {self.stop_number}:{self.stop_name}"
    
    def save(self, *args, **kwargs):
        if self.stop_number == 1:
            self.fare_from_start = 0
        super().save(*args, **kwargs)


class Booking(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    no_of_seats = models.PositiveIntegerField()
    bus = models.ForeignKey(busdetails, on_delete=models.CASCADE)
    source_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='bookings_from', null=True)
    destination_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='bookings_to',null=True)
    is_cancelled = models.BooleanField(default=False)

    @property
    def email(self):
        return self.name.email

    def calculate_far(self):
        return self.destination_stop.fare_from_start - self.source_stop.fare_from_start

    def __str__(self):
        return f'{self.name} has booked {self.no_of_seats}seats in bus:{self.bus} on {self.date} '

class Passenger(models.Model):
    Genders = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="passengers")
    name = models.CharField(max_length=500)
    age = models.PositiveIntegerField(default=20)
    gender = models.CharField(max_length=1, choices=Genders,default='F')

    def __str__(self):
        return f'{self.name} in {self.booking.bus}'


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)
