from djongo import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from informacionesEconomicas.models import InformacionEconomica
from django.conf import settings

class Cliente(models.Model):
    # e
    cedula = models.CharField(max_length=512, primary_key=True, unique=True)
    # h
    cedulaHash = models.CharField(max_length=256, null=True, blank=True)
    nombres = models.CharField(max_length=256)
    apellidos = models.CharField(max_length=256)
    # e
    celular = models.CharField(max_length=512, unique=True)
    # h
    celularHash = models.CharField(max_length=256, null=True, blank=True)
    # e
    correo = models.CharField(max_length=512, unique=True)
    # h
    correoHash = models.CharField(max_length=256, null=True, blank=True)
    pais = models.CharField(max_length=256)
    ciudad = models.CharField(max_length=256)
    # e
    direccion = models.CharField(max_length=512)
    # e futuro
    fechaNacimiento = models.DateField()

    infoEconomica = models.OneToOneField(InformacionEconomica, null=True, blank=True, default=None, on_delete=models.CASCADE)
    solicitud = models.IntegerField(null=True, blank=True, default=None)

    @property
    def cedula_decrypted(self):
        return settings.F.decrypt(self.cedula.encode('utf-8')).decode('utf-8')
    
    @property
    def celular_decrypted(self):
        return settings.F.decrypt(self.celular.encode('utf-8')).decode('utf-8')
    
    @property
    def correo_decrypted(self):
        return settings.F.decrypt(self.correo.encode('utf-8')).decode('utf-8')
    
    @property
    def direccion_decrypted(self):
        return settings.F.decrypt(self.direccion.encode('utf-8')).decode('utf-8')
    
    def __str__(self):
        return '{}'.format(self.cedula)
        
    def clean(self):
        try:
            validate_email(self.correo)
        except ValidationError:
            raise ValidationError('Correo no válido')

