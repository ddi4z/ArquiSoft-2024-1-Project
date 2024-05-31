from django import forms
from .models import Solicitud

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'etapaActual',
            'lugarSolicitud'
        ]

        labels = {
            'etapaActual' : 'Etapa actual',
            'lugarSolicitud' : 'Lugar de la solicitud'
        }
