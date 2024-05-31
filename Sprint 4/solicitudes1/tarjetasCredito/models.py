from django.db import models

from tarjetasOfertadas.models import TarjetaOfertada
from solicitudes.models import Solicitud
from django.conf import settings
from dj_cqrs.mixins import MasterMixin

class TarjetaCredito(MasterMixin, models.Model):
    CQRS_ID = 'tarjeta_credito_model'

    # e
    numero = models.CharField(max_length=512, primary_key=True, unique=True)
    # h
    numeroHash = models.CharField(max_length=256, null=True, blank=True)
    # e futuro
    activada = models.BooleanField()
    # e futuro
    fechaAdquisicion = models.DateField(auto_now_add=True)
    # e futuro
    fechaVencimiento = models.DateField()

    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    tipoTarjeta = models.OneToOneField(TarjetaOfertada, on_delete=models.CASCADE, related_name='tarjetaCredito')

    class Meta:
        verbose_name_plural = "tarjetas credito"

    def __str__(self):
        return '{}'.format(self.numero)
    
    @property
    def numero_decrypted(self):
        return settings.F.decrypt(self.numero.encode('utf-8')).decode('utf-8')
