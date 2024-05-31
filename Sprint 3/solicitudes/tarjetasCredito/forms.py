from django import forms
from .models import TarjetaCredito

class PagareForm(forms.ModelForm):
    class Meta:
        model = TarjetaCredito
        fields = [
            'numero',
            'activada',
            'fechaVencimiento',
        ]

        labels = {
            'numero': 'Número',
            'activada': 'Activada',
            'fechaVencimiento': 'Fecha de vencimiento',
        }
