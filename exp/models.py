from django.contrib.auth.models import User
import datetime
from django.db import models


class busdetails(models.Model):
    """Seat_Categories = (
        ('GEN', 'general'),
        ('SLP', 'sleeper'),
        ('LXY', 'luxury'),
    )"""
    bus_name = models.CharField(max_length=50)
    bus_number = models.CharField(max_length=10)
    depart_from = models.CharField(max_length=50)
    stop1 = models.CharField(max_length=50)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField()
    totalseats = models.IntegerField()
    availableseats = models.IntegerField(default=150)
    fare = models.IntegerField()

    # category = models.CharField(max_length=3, choices=Seat_Categories)

    # def __str__(self):
    #     return f' {self.bus_name}'


class Booking(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    no_of_seats = models.IntegerField()
    bus = models.ForeignKey(busdetails, on_delete=models.CASCADE)

    @property
    def email(self):
        return self.name.email

    def __str__(self):
        return f'{self.name} has booked {self.no_of_seats}seats in bus:{self.bus} on {self.date} '


class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="passengers")
    name = models.CharField(max_length=500)

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
