
# # Import necessary modules
from django.contrib import admin
# from django import forms
from .models import Bus, Seat, Ticket


admin.site.register(Bus)
admin.site.register(Seat)
admin.site.register(Ticket)


