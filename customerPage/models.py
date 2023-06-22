from django.db import models

from django.contrib.auth.models import AbstractUser



class Customer(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)

class UserPayment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_intent_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment ID: {self.pk}, User: {self.user.username}, Amount: {self.amount}"








