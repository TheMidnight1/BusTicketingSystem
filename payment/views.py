import stripe
import json
from .models import Payment
from django.urls import reverse
from django.conf import settings
from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpResponseNotFound
from Bus.models import Bus, Seat, Ticket
from .utils import generate_ticket_number
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from reportlab.lib.pagesizes import A4
from Bus.pusher import pusher_client
from django.contrib.auth.decorators import login_required

from Bus.redis import r





from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    selected_seats = request.POST.getlist('seats_selected')
    pusher_client.trigger("bus-channel",'seats-updated',{'bus_id':bus.pk,'seats':selected_seats,"action":"lock"})
    
    print(selected_seats)
    total_amount = len(selected_seats) * bus.price

    if request.method == 'POST':
        user_id = request.user.id
        # set a locker in redis cache
        key = f"bus:{pk}:{user_id}"
        r.setex(key,180,json.dumps(selected_seats))
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),  # Stripe requires the amount in cents
                currency='usd',
            )
            client_secret = intent.client_secret
            
        except stripe.error.CardError as e:
            # Display error message to the user
            pass
    else:
        client_secret = None

    return render(request, 'checkout.html', {
        'bus': bus,
        'selected_seats': selected_seats,
        'total_amount': total_amount,
        'client_secret': client_secret,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        bus_name = request.POST.get('bus_name')
        bus_number = request.POST.get('bus_number')
        selected_seats = request.POST.getlist('selected_seats')

        bus_details = {'bus_name':bus_name , 'bus_number':bus_number}
        seat_numbers = []
        for seat in selected_seats:
            seat_numbers.extend(eval(seat))

        # Convert seat numbers to integers
        seat_numbers = [int(number.strip()) for number in seat_numbers]

        amount = float(request.POST.get('amount'))
        bus_id = request.POST.get('bus_id')

        # Retrieve the bus object
        bus = Bus.objects.get(pk=bus_id)

        # Save the payment details to the database
        payment = Payment.objects.create(
            user=user,
            bus_name=bus_name,
            bus_number=bus_number,
            bus=bus,  # Assign the bus object to the bus field
            selected_seats=selected_seats,
            amount=amount,
        )

        # Generate ticket numbers and create tickets
        ticket_numbers = [generate_ticket_number() for _ in seat_numbers]

        tickets = []
        for seat_number, ticket_number in zip(seat_numbers, ticket_numbers):
            print("TICKET NUMBER")
            print(ticket_number)
            # Retrieve or create the seat object
            seat, created = Seat.objects.get_or_create(bus=bus, number=seat_number)

            # Set the seat as unavailable and save it
            seat.is_available = False
            seat.booked_by = request.user

            # Save the seat object individually
            seat.save()

            # Create a new ticket object
            ticket = Ticket(ticket_number=ticket_number, seat=seat, bus=bus)
            ticket.save()
            tickets.append(ticket)
        print(tickets)

        ticket_number_query = '&'.join(['ticket_numbers=' + number for number in ticket_numbers])
        # Generate the URL for download_pdf view with the ticket_number argument
        download_url = reverse('payment:download_pdf') + '?' + ticket_number_query

        return render(request, 'payment_success.html', {
            'ticket_numbers': ticket_numbers,
            'download_url': download_url,
            'bus_details':bus_details
        })



def download_pdf(request):
    ticket_numbers = request.GET.getlist('ticket_numbers')
    
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tickets.pdf"'

    # Create the PDF document
    p = canvas.Canvas(response,pagesize=A4)

    for ticket_number in ticket_numbers:
        try:
            ticket = Ticket.objects.get(ticket_number=ticket_number)
        except Ticket.DoesNotExist:
            return HttpResponseNotFound('Ticket not found.')

        # Write the ticket details to the PDF
        p.drawString(100, 100, f'Ticket Number: {ticket.ticket_number}')
        p.drawString(100, 120, f'Bus Name: {ticket.bus.name}')
        p.drawString(100, 140, f'Bus Number: {ticket.bus.bus_number}')
        p.drawString(100, 160, f'Source: {ticket.bus.source}')
        p.drawString(100, 180, f'Destination: {ticket.bus.destination}')
        p.drawString(100, 200, f'Operator Details: {ticket.bus.operator_details}')
        p.drawString(100, 220, f'Travel Dates: {ticket.bus.travel_dates}')
        p.drawString(100, 240, f'Seat Number: {ticket.seat.number}')

        # Add other ticket details as needed

        # Move to the next page for the next ticket
        p.showPage()

    # Save the PDF document
    p.save()

    return response


def booking_history(request):
    user = request.user
    payments = Payment.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'booking_history.html', {'payments': payments})





class BookedSeatsView(ListView):
    template_name = 'booked_history.html'
    context_object_name = 'payments'
    queryset = Payment.objects.all()