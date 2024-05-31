from django.db import models

from validacionesManuales.models import ValidacionManual
from django.conf import settings

class DocumentoValidado(models.Model):

    class TipoDocumento(models.TextChoices):
        CEDULA_FRONTAL = 'CEDULA_FRONTAL', 'CEDULA_FRONTAL'
        CEDULA_POSTERIOR = 'CEDULA_POSTERIOR', 'CEDULA_POSTERIOR'
        DESPRENDIBLE_PAGO = 'DESPRENDIBLE_PAGO', 'DESPRENDIBLE_PAGO'

    class DescripcionConfiabilidad(models.TextChoices):
        CONFIABLE = 'CONFIABLE', 'CONFIABLE'
        NO_CONFIABLE = 'NO_CONFIABLE', 'NO_CONFIABLE'

    tipo = models.CharField(max_length=256, choices=TipoDocumento.choices)
    # e
    ruta = models.CharField(max_length=512)
    # e futuro
    score = models.FloatField()
    descripcion = models.CharField(max_length=256, choices=DescripcionConfiabilidad.choices, default=DescripcionConfiabilidad.NO_CONFIABLE)
    fechaAutovalidacion = models.DateTimeField(auto_now_add=True)

    # TODO: CONECTARSE CON SOLICITUD, ESTE ATRIBUTO ES UN INTEGER (LLAVE FORÁNEA)
    #solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    validacionManual = models.OneToOneField(ValidacionManual, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "documentos validados"

    def __str__(self):
        return '{}'.format(self.id)
    
    @property
    def ruta_decrypted(self):
        return settings.F.decrypt(self.ruta.encode('utf-8')).decode('utf-8')
