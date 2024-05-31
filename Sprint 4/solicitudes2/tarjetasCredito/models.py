from django.db import models

from tarjetasOfertadas.models import TarjetaOfertada
from solicitudes.models import Solicitud
from django.conf import settings
from dj_cqrs.mixins import ReplicaMixin

class TarjetaCredito(ReplicaMixin, models.Model):
    CQRS_ID = 'tarjeta_credito_model'
    CQRS_CUSTOM_SERIALIZATION = True

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
    
    @staticmethod
    def _handle_solicitud(mapped_data):
        solicitud = Solicitud.objects.get(pk=mapped_data)
        return solicitud
    
    @staticmethod
    def _handle_tipoTarjeta(mapped_data):
        tipoTarjeta = TarjetaOfertada.objects.get(pk=mapped_data)
        return tipoTarjeta

    @classmethod
    def cqrs_create(cls, sync, mapped_data, previous_data=None, meta=None):
        solicitud = cls._handle_solicitud(mapped_data['solicitud'])
        tipoTarjeta = cls._handle_tipoTarjeta(mapped_data['tipoTarjeta'])
        return TarjetaCredito.objects.create(
            id=mapped_data['id'],
            numero=mapped_data['numero'],
            numeroHash=mapped_data['numeroHash'],
            activada=mapped_data['activada'],
            fechaAdquisicion=mapped_data['fechaAdquisicion'],
            fechaVencimiento=mapped_data['fechaVencimiento'],
            solicitud=solicitud,
            tipoTarjeta=tipoTarjeta,
            cqrs_revision=mapped_data['cqrs_revision'],
            cqrs_updated=mapped_data['cqrs_updated'],
        )
    
    def cqrs_update(self, sync, mapped_data, previous_data=None, meta=None):
        solicitud = self._handle_solicitud(mapped_data['solicitud'])
        tipoTarjeta = self._handle_tipoTarjeta(mapped_data['tipoTarjeta'])
        self.numero = mapped_data['numero']
        self.numeroHash = mapped_data['numeroHash']
        self.activada = mapped_data['activada']
        self.fechaAdquisicion = mapped_data['fechaAdquisicion']
        self.fechaVencimiento = mapped_data['fechaVencimiento']
        self.solicitud = solicitud
        self.tipoTarjeta = tipoTarjeta
        self.cqrs_revision = mapped_data['cqrs_revision']
        self.cqrs_updated = mapped_data['cqrs_updated']
        self.save()
        return self
