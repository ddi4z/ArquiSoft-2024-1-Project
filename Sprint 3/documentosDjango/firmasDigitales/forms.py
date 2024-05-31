from django import forms
from models import FirmaDigital

class FirmaDigitalForm(forms.ModelForm):
    class Meta:
        model = FirmaDigital
        fields = [
            'ruta', 
        ]

        labels = {
            'ruta' : 'Ruta',
        }