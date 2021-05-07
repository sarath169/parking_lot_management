from django import forms
from django.contrib.auth.forms import UserCreationForm
from  parking.models import ParkingHistory


class QRForm(forms.Form):
    qrdata = forms.CharField(label='QR Data',max_length=12)
