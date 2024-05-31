from django.db import models
from tarjetasDisponibles.models import TarjetaDisponible
from solicitudes.models import Solicitud

class TarjetaOfertada(models.Model):
    # e futuro
    cupo = models.PositiveIntegerField()
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    tarjetaDisponible = models.ForeignKey(TarjetaDisponible, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "tarjetas ofertadas"

    def __str__(self):
        return '{}'.format(self.id)
