from django import forms
from models import Log

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = [
            'nombreEvento', 
            'codigoHTTP',
            'metodoHTTP',
            'direccionIP',
        ]

        labels = {
            'nombreEvento' : 'Nombre del evento',
            'codigoHTTP' : 'Código HTTP',
            'metodoHTTP' : 'Método HTTP',
            'direccionIP' : 'Dirección IP',
        }