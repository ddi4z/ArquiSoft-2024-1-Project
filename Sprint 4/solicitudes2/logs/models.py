from django.db import models
from django.conf import settings
from solicitudes.models import Solicitud
from dj_cqrs.mixins import ReplicaMixin

class Log(ReplicaMixin, models.Model):
    CQRS_ID = 'log_model'
    CQRS_CUSTOM_SERIALIZATION = True

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
    
    @staticmethod
    def _handle_solicitud(mapped_data):
        solicitud = Solicitud.objects.get(pk=mapped_data)
        return solicitud
    
    @classmethod
    def cqrs_create(cls, sync, mapped_data, previous_data=None, meta=None):
        return Log.objects.create(
            id=mapped_data['id'],
            fecha=mapped_data['fecha'],
            nombreEvento=mapped_data['nombreEvento'],
            codigoHTTP=mapped_data['codigoHTTP'],
            metodoHTTP=mapped_data['metodoHTTP'],
            direccionIP=mapped_data['direccionIP'],
            cqrs_revision=mapped_data['cqrs_revision'],
            cqrs_updated=mapped_data['cqrs_updated'],
        )
    
    def cqrs_update(self, sync, mapped_data, previous_data=None, meta=None):
        self.fecha = mapped_data['fecha']
        self.nombreEvento = mapped_data['nombreEvento']
        self.codigoHTTP = mapped_data['codigoHTTP']
        self.metodoHTTP = mapped_data['metodoHTTP']
        self.direccionIP = mapped_data['direccionIP']
        self.cqrs_revision = mapped_data['cqrs_revision']
        self.cqrs_updated = mapped_data['cqrs_updated']
        self.save()
        return self