from django import forms
from .models import Pagare

class PagareForm(forms.ModelForm):
    class Meta:
        model = Pagare
        fields = [
            'ruta',
        ]

        labels = {
            'ruta' : 'Ruta',
        }
