import time
import json

from .redis import r
from .models import Booking
from .models import Bus,Seat
from datetime import datetime
from .forms import SearchForm
from .pusher import pusher_client
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

    
def search_view(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            source = form.cleaned_data['source']
            destination = form.cleaned_data['destination']
            travel_date = form.cleaned_data['travel_date']
            
            # Convert travel_date to datetime object
            travel_datetime = datetime.combine(travel_date, datetime.min.time())
            
            # Query the Bus model to find matching buses
            matching_buses = Bus.objects.filter(
                source__icontains=source,
                destination__icontains=destination,
                travel_dates=travel_datetime,
            )
            
            return render(request, 'bus.html', {'matching_buses': matching_buses})
    else:
        form = SearchForm()

    return render(request, 'home.html', {'form': form})



def book_seats(request):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('selected_seats[]')
        user_id = request.user.id
        # r.hset(f"bus:{}")
        print("yei ho yei ho")
        for seat_number in selected_seats:
            booking = Booking(seat_number=int(seat_number))
            booking.save()
        return render(request, 'confirm_booking.html')
    else:
        return render(request, 'seat.html')



def seats(request,pk):

    # Retrieve the bus object
    bus = get_object_or_404(Bus, pk=pk)
     # Retrieve the seat object of this bus
    all_seats = Seat.objects.filter(bus=bus)
    seat_numbers = list(map(lambda seat: seat.number, all_seats))
    # if request.method == 'POST':
    #     selected_seats = request.POST.getlist('seats_selected')

       
        
    #     # Iterate over the selected seats
    #     # for seat_number in selected_seats:
    #         # seat_number = seat_number.strip()
            
    #         # Retrieve or create the seat object
    #         # seat, created = Seat.objects.get_or_create(bus=bus, number=seat_number)
            
    #         # Set the seat as unavailable and save it
    #         # seat.is_available = False
    #         # seat.booked_by = request.user
    #         # seat.save()

    #     all_seats = Seat.objects.filter(bus=bus)
    #     seat_numbers = list(map(lambda seat: seat.number, all_seats))
    #     return render(request, 'seat.html', {'seats': range(1, 9),'bus':bus,'booked_seats': seat_numbers })
    
    locked = []
    keys = r.keys(f"bus:{pk}:*")
    if keys:
        for key in keys:
            seats = r.get(key)            
            if seats: locked = locked +json.loads(seats)
                      
    return render(request, 'seat.html', {'seats': range(1, 9),'bus':bus,'booked_seats': seat_numbers + locked })
    
@login_required
def confirm_booking(request):
    selected_seats = request.POST.getlist('selected_seats[]')
    # selected_seats = json.loads(request.POST.get('selected_seats'))
    

    return render(request, 'confirm_booking.html', {'selected_seats': selected_seats})

@login_required
def cancel_booking(request):
    bus_id = request.POST.get('bus_id')
    selected_seats = []
    key =f"bus:{bus_id}:{request.user.id}"
    seats = r.get(key)
    if seats:
        selected_seats = json.loads(seats)
        r.delete(key)
    pusher_client.trigger("bus-channel",'seats-updated',{'bus_id':bus_id,'seats':selected_seats,"action":"unlock"})

    return redirect(f"/seats/{bus_id}")




