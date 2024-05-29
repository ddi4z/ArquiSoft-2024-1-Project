from django.db import models
from django.conf import settings
from dj_cqrs.mixins import ReplicaMixin

class Solicitud(ReplicaMixin, models.Model):
    CQRS_ID = 'solicitud_model'

    class Etapa(models.TextChoices):
        INFORMACION_ECONOMICA = 'INFORMACION_ECONOMICA', 'INFORMACION_ECONOMICA'
        PRESENTACION_OFERTA = 'PRESENTACION_OFERTA', 'PRESENTACION_OFERTA'
        VALIDACION_LUGAR = 'VALIDACION_LUGAR', 'VALIDACION_LUGAR'
        FIRMA_DOCUMENTOS = 'FIRMA_DOCUMENTOS', 'FIRMA_DOCUMENTOS'
        CARGUE_DOCUMENTOS = 'CARGUE_DOCUMENTOS', 'CARGUE_DOCUMENTOS'
        CONFIRMACION = 'CONFIRMACION', 'CONFIRMACION'
        ACTIVACION = 'ACTIVACION', 'ACTIVACION'

    class LugarSolicitud(models.TextChoices):
        APLICACION = 'APLICACION', 'APLICACION'
        SUCURSAL_BANCARIA = 'SUCURSAL_BANCARIA', 'SUCURSAL_BANCARIA'    

    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaUltimaModificacion = models.DateTimeField(auto_now_add=True)
    etapaActual = models.CharField(max_length=256, choices=Etapa.choices, default=Etapa.INFORMACION_ECONOMICA)
    lugarSolicitud = models.CharField(max_length=256, choices=LugarSolicitud.choices, default=LugarSolicitud.APLICACION)

    pagare = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "solicitudes"

    def __str__(self):
        return '{}'.format(self.id)
    