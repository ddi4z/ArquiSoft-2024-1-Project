from django import forms
from models import TarjetaOfertada

class TarjetaOfertadaForm(forms.ModelForm):
    class Meta:
        model = TarjetaOfertada
        fields = [
            'cupo',
        ]

        labels = {
            'cupo' : 'Cupo',
        }