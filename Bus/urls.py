from django.urls import path
from .views import book_seats,seats,confirm_booking, search_view

app_name = "Bus"
urlpatterns = [
    path('search/', search_view, name='search'),
    path('book-seats/', book_seats, name='book_seats'),
    path('seats/<int:pk>', seats, name='seats'),
    path('confirm-booking/', confirm_booking, name='confirm_booking'),


]
