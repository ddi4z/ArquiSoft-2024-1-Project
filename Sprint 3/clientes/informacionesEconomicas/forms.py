from django import forms
from .models import InformacionEconomica

class InformacionEconomicaForm(forms.ModelForm):
    class Meta:
        model = InformacionEconomica
        fields = [
            'profesion',
            'actividadEconomica',
            'empresa',
            'ingresos',
            'egresos',
            'deudas',
            'patrimonio',

        ]

        labels = {
            'profesion': 'Profesión',
            'actividadEconomica': 'Actividad económica',
            'empresa': 'Empresa',
            'ingresos': 'Ingresos',
            'egresos': 'Egresos',
            'deudas': 'Deudas',
            'patrimonio': 'Patrimonio',
        }
