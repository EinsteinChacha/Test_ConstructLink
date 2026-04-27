from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import BookingRequest, Equipment, User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'account_type', 'password1', 'password2')


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'category',
            'name',
            'description',
            'region',
            'district',
            'daily_price',
            'availability_status',
            'photo',
        ]


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['start_date', 'end_date', 'site_location', 'purpose_of_use', 'contact_phone']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
