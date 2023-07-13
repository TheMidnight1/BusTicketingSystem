from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from customerPage.forms import UserForm,LoginForm, EditForm, ChangePasswordForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView , PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


from django.http import HttpResponse, HttpResponseBadRequest
from Bus.models import Ticket, Seat




# Create your views here.



def RegisterPage(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customerPage:login')    # Redirect to the login page after successful registration
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


class MyLoginView(LoginView):
    form_class = LoginForm
    
    template_name = "login.html"


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = EditForm
    template_name = "editProfile.html"
    success_url = reverse_lazy("customerPage:profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["password_form"] = ChangePasswordForm(
                self.request.user, self.request.POST
            )
        else:
            context["password_form"] = ChangePasswordForm(self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        password_form = context["password_form"]
        if password_form.is_valid():
            password_form.save()
        return super().form_valid(form) 

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "change_password.html"
    form_class = ChangePasswordForm
    context_object_name = "form"
    success_url = reverse_lazy("customerPage:profile")


def Index(request):
    return render(request, 'home.html')

class Logout(LogoutView):
    next_page = reverse_lazy("customerPage:login")

def Profile(request):
    return render(request, 'profile.html')



def Cancel(request):
    if request.method == 'POST':
        ticket_number = request.POST.get('ticket_no')

        try:
            ticket = Ticket.objects.get(ticket_number=ticket_number)
            seat = ticket.seat  # Assign the seat instance to the seat variable

            # Mark the seat as available again
            seat.delete()


            # Delete the ticket
            ticket.delete()

            return render(request, 'ticket_cancel_success.html')
        except Ticket.DoesNotExist:
            messages.error(request, 'Invalid ticket number. Please try again.')

    return render(request, 'cancel.html')






def Print(request):
    return render(request, 'printTicket.html')

def About(request):
    return render(request, 'aboutUs.html')

def Contact(request):
    return render(request, 'contactUs.html')











