
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import RadioSelect, SelectDateWidget
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm


from .models import Customer







User = get_user_model()


def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError(_("Invalid phone number. Please enter only digits."))
    if len(value) != 10:
        raise ValidationError(
            _("Invalid phone number. The phone number must have 10 digits.")
        )


def validate_first_name(value):
    if value.isdigit():
        raise ValidationError(_("Invalid . Please enter only alphabets."))
    # if len(value)>4:
    #     raise ValidationError(_('Invalid first name. First name should be more than 4 and less than character.'))

    # raise ValidationError(_('Invalid first name. First name should be less than 30 character.'))


def validate_last_name(value):
    if value.isdigit():
        raise ValidationError(_("Invalid . Please enter only alphabets."))
    # if len(value) >4:
    #     raise ValidationError(_('Invalid last name. Last name should be more than 4 character.'))
    # if len(value) <30:
    #     raise ValidationError(_('Invalid last name. First name should be less than 30 character.'))


class UserForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[validate_phone_number],
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        validators=[EmailValidator(message="Please enter a valid email address.")],
    )
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[validate_first_name],
    )
    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[validate_last_name],
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]
        widgets = {
            "date_of_birth": SelectDateWidget(years=range(1923, 2023)),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'name': 'username', 'class': 'form-control', 'autofocus': True}))
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'name': 'password','class': 'form-control'}))


class EditForm(UserChangeForm):
    class Meta:
        model = get_user_model()  # Call the get_user_model function
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password")
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "appearance-none block w-full py-2 px-3 leading-tight border border-gray-300 rounded focus:outline-none focus:bg-white focus:border-gray-500"
                }
            )

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("old_password", "new_password1", "new_password2")



