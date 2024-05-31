from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'cedula', 
            'nombres',
            'apellidos',
            'celular',
            'correo',
            'pais',
            'ciudad',
            'direccion',
            'fechaNacimiento',
        ]

        labels = {
            'cedula' : 'Cédula',
            'nombres' : 'Nombres',
            'apellidos' : 'Apellidos',
            'celular' : 'Celular',
            'correo' : 'Correo',
            'pais' : 'País',
            'ciudad' : 'Ciudad',
            'direccion' : 'Dirección',
            'fechaNacimiento' : 'Fecha de nacimiento',
        }

        widgets = {
            'fechaNacimiento': forms.DateInput(attrs={'type': 'date'})
        }