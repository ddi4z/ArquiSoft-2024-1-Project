from django import forms
from models import ValidacionManual

class ValidacionManualForm(forms.ModelForm):
    class Meta:
        model = ValidacionManual
        fields = [
            'aprobado',
            'descripcion',
            'fechaValidacion',
        ]

        labels = {
            'aprobado' : 'Aprobado',
            'descripcion' : 'Descripción',
            'fechaValidacion' : 'Fecha de validación',
        }