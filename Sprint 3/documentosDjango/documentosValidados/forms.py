from django import forms
from .models import DocumentoValidado

class DocumentoValidadoForm(forms.ModelForm):
    class Meta:
        model = DocumentoValidado
        fields = [
            'tipo',
            'ruta',
            'score',
            'descripcion',
        ]

        labels = {
            'tipo' : 'Tipo',
            'ruta' : 'Ruta',
            'score' : 'Score',
            'descripcion' : 'Descripción',
        }
