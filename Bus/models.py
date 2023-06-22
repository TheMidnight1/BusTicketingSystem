from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Bus(models.Model):
    name = models.CharField(max_length=50)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    travel_dates = models.DateField(_("Travel Dates"), auto_now=False, auto_now_add=False)
    features = models.TextField()
    image = models.ImageField(upload_to='')  
    bus_number = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    departure_time = models.TimeField()
    pickup_location = models.CharField(max_length=100)
    drop_location = models.CharField(max_length=100)
    operator_details = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.source} to {self.destination}"




class Seat(models.Model):
    number = models.CharField(max_length=10)
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.number

class Booking(models.Model):
    seat_number = models.IntegerField()

    def __str__(self):
        return str(self.seat_number)




class Ticket(models.Model):
    ticket_number = models.CharField(max_length=20)
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    seat = models.ForeignKey('Seat', on_delete=models.CASCADE)  # Add this field


    def __str__(self):
        return self.ticket_number
