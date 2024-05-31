from django import forms
from .models import TarjetaDisponible

class TarjetaDisponibleForm(forms.ModelForm):
    class Meta:
        model = TarjetaDisponible
        fields = [
            'perfil',
            'franquicia',
            'imagen',
            'descripcion',
            'tiempoVigenciaMeses',
        ]

        labels = {
            'perfil' : 'Perfil',
            'franquicia' : 'Franquicia',
            'imagen' : 'Imagen',
            'descripcion' : 'Descripcion',
            'tiempoVigenciaMeses' : 'Tiempo de vigencia en meses',
        }
