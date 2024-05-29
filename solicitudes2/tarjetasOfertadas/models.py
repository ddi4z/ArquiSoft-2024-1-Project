from django.db import models
from tarjetasDisponibles.models import TarjetaDisponible
from solicitudes.models import Solicitud
from dj_cqrs.mixins import ReplicaMixin

class TarjetaOfertada(ReplicaMixin, models.Model):
    CQRS_ID = 'tarjeta_ofertada_model'
    CQRS_CUSTOM_SERIALIZATION = True

    # e futuro
    cupo = models.PositiveIntegerField()
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    tarjetaDisponible = models.ForeignKey(TarjetaDisponible, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "tarjetas ofertadas"

    def __str__(self):
        return '{}'.format(self.id)
    
    @staticmethod
    def _handle_solicitud(mapped_data):
        solicitud = Solicitud.objects.get(pk=mapped_data)
        return solicitud
    
    @staticmethod
    def _handle_tarjetaDisponible(mapped_data):
        tarjetaDisponible = TarjetaDisponible.objects.get(pk=mapped_data)
        return tarjetaDisponible
    
    @classmethod
    def cqrs_create(cls, sync, mapped_data, previous_data=None, meta=None):
        solicitud = cls._handle_solicitud(mapped_data['solicitud'])
        tarjetaDisponible = cls._handle_tarjetaDisponible(mapped_data['tarjetaDisponible'])
        return TarjetaOfertada.objects.create(
            id=mapped_data['id'],
            cupo=mapped_data['cupo'],
            solicitud=solicitud,
            tarjetaDisponible=tarjetaDisponible,
            cqrs_revision=mapped_data['cqrs_revision'],
            cqrs_updated=mapped_data['cqrs_updated'],
        )
    
    def cqrs_update(self, sync, mapped_data, previous_data=None, meta=None):
        solicitud = self._handle_solicitud(mapped_data['solicitud'])
        tarjetaDisponible = self._handle_tarjetaDisponible(mapped_data['tarjetaDisponible'])
        self.cupo = mapped_data['cupo']
        self.solicitud = solicitud
        self.tarjetaDisponible = tarjetaDisponible
        self.cqrs_revision = mapped_data['cqrs_revision']
        self.cqrs_updated = mapped_data['cqrs_updated']
        self.save()
        return self
