from ..models import TarjetaOfertada
import random
from tarjetasDisponibles.models import TarjetaDisponible

def get_tarjeta_ofertada_by_id(id):
    queryset = TarjetaOfertada.objects.filter(id=id)
    return queryset.first()

def get_tarjetas_ofertadas():
    queryset = TarjetaOfertada.objects.all()
    return (queryset)

def get_tarjetas_ofertadas_by_solicitud(solicitud):
    queryset = TarjetaOfertada.objects.filter(solicitud=solicitud)
    if not queryset.exists():
        create_tarjeta_ofertada(solicitud, "VISA")
        create_tarjeta_ofertada(solicitud, "MASTERCARD")
    queryset = TarjetaOfertada.objects.filter(solicitud=solicitud)
    return queryset

def create_tarjeta_ofertada(solicitud, franquicia):
    tarjeta = TarjetaOfertada()
    tarjeta.cupo = 1000000
    tarjeta.solicitud = solicitud
    if franquicia == "VISA":
        tarjeta.tarjetaDisponible = TarjetaDisponible.objects.all()[random.randint(0, 3)]
    else:
        tarjeta.tarjetaDisponible = TarjetaDisponible.objects.all()[random.randint(4, 7)]
    tarjeta.save()
    solicitud.save()
    return tarjeta
    
