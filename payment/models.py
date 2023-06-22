from django.db import models
from Bus.models import Bus
# Create your models here.
# models.py


class Payment(models.Model):
    user = models.CharField(max_length=255)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    bus_name = models.CharField(max_length=255)
    bus_number = models.CharField(max_length=255)
    selected_seats = models.TextField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.bus_name} ({self.timestamp})"
