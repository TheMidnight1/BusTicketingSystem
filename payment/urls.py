from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('booked-seats/', views.BookedSeatsView.as_view(), name='booked_seats'),
    path('booking_history/', views.booking_history, name='booking_history'),
    path('download_pdf/', views.download_pdf, name='download_pdf')

    
]
