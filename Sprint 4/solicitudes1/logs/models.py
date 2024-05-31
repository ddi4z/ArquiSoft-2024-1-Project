from django.db import models
from django.conf import settings
from solicitudes.models import Solicitud
from dj_cqrs.mixins import MasterMixin

class Log(MasterMixin, models.Model):
    CQRS_ID = 'log_model'

    fecha = models.DateTimeField(auto_now_add=True)
    # e
    nombreEvento = models.CharField(max_length=512)
    codigoHTTP = models.CharField(max_length=256)
    metodoHTTP = models.CharField(max_length=256)
    # e
    direccionIP = models.CharField(max_length=512)

    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)

    @property
    def nombreEvento_decrypted(self):
        return settings.F.decrypt(self.nombreEvento.encode('utf-8')).decode('utf-8')

    @property
    def direccionIP_decrypted(self):
        return settings.F.decrypt(self.direccionIP.encode('utf-8')).decode('utf-8')