from django.shortcuts import render,get_object_or_404,redirect
from .forms import BusForm,SeatForm
from Bus.models import Bus,Seat


def Home1(request):
    return render(request, 'home1.html')

def createBus(request):
    if request.method == 'POST':
        form = BusForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('/adminpage')  # Redirect to a success page
    else:
        form = BusForm()

    return render(request, 'createBus.html', {'form': form})

def seatBook(request):
    busses = Bus.objects.all()

    if request.method == 'POST':
        selected_seats = request.POST.getlist('selected_seats')
        # Process the selected seats data, such as saving it to the database
        # You can access the selected seats using the `selected_seats` list

    # Bus search functionality
    search_query = request.GET.get('bus_number')
    if search_query:
        busses = busses.filter(bus_number__icontains=search_query)

    return render(request, 'seatbook.html', {'busses': busses})



def bookSeat(request, pk):
     # Retrieve the bus object
    bus = get_object_or_404(Bus, pk=pk)
    
     # Retrieve the seat object of this bus
    all_seats = Seat.objects.filter(bus=bus)
    seat_numbers = list(map(lambda seat: seat.number, all_seats))
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats_selected')
        

        
        # Iterate over the selected seats
        for seat_number in selected_seats:
            seat_number = seat_number.strip()
            
            # Retrieve or create the seat object
            seat, created = Seat.objects.get_or_create(bus=bus, number=seat_number)
            
            # Set the seat as unavailable and save it
            seat.is_available = False
            seat.booked_by = request.user
            seat.save()

        all_seats = Seat.objects.filter(bus=bus)
        seat_numbers = list(map(lambda seat: seat.number, all_seats))
        # Render the success template with the bus and booked seats
        return render(request, 'bookSeat.html', {'seats': range(1, 9),'bus': bus, 'booked_seats': seat_numbers})

    else:
        # If the request method is not POST, render the booking form
        return render(request, 'bookSeat.html', {'seats': range(1, 9), 'bus': bus,'booked_seats': seat_numbers})


