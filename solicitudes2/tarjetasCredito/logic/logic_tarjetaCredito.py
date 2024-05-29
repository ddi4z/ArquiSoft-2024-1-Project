from ..models import TarjetaCredito
import random
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.conf import settings
import hashlib
import time

def get_tarjetas_credito():
    queryset = TarjetaCredito.objects.all()
    return (queryset)

def get_tarjeta_credito_by_solicitud(solicitud):
    queryset = TarjetaCredito.objects.filter(solicitud=solicitud)
    return queryset.first()

def create_tarjeta_credito(tarjetaOfertada):
    tarjeta = TarjetaCredito()
    tarjeta.solicitud = tarjetaOfertada.solicitud
    tarjeta.tipoTarjeta = tarjetaOfertada
    numero_random = list(str(random.randint(0, 99999999)).zfill(8) + str(tarjeta.solicitud.id).zfill(8))
    numero_formateado = []
    for i in range(4):
        numero_formateado.append("".join(numero_random[i*4:(i+1)*4]))

    inicio = time.time()
    tarjeta.numero = settings.F.encrypt("-".join(numero_formateado).encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando tarjeta: {time.time() - inicio}")
    
    inicio = time.time()
    tarjeta.numeroHash = hashlib.sha256("-".join(numero_formateado).encode('utf-8')).hexdigest()
    print(f"Tiempo hasheando tarjeta: {time.time() - inicio}")
    
    fecha = timezone.now()
    tarjeta.fechaAdquisicion = fecha 
    tarjeta.fechaVencimiento = fecha + relativedelta(months=tarjetaOfertada.tarjetaDisponible.tiempoVigenciaMeses)
    tarjeta.activada = False
    tarjeta.full_clean()
    tarjeta.save()
    tarjetaOfertada.full_clean()
    tarjetaOfertada.save()
    return tarjeta
