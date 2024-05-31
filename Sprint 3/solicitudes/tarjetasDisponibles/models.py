from django.db import models
from django.conf import settings

class TarjetaDisponible(models.Model):
    perfil = models.CharField(max_length=256)
    franquicia = models.CharField(max_length=256)
    imagen = models.CharField(max_length=256)
    # e
    descripcion = models.CharField(max_length=512)
    # e futuro
    tiempoVigenciaMeses = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "tarjetas disponibles"

    def __str__(self):
        return '{}'.format(self.id)
    
    @property
    def descripcion_decrypted(self):
        return settings.F.decrypt(self.descripcion.encode('utf-8')).decode('utf-8')
    