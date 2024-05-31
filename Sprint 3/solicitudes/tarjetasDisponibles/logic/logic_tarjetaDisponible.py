from ..models import TarjetaDisponible
from django.conf import settings
import time

def get_tarjetas_disponibles():
    queryset = TarjetaDisponible.objects.all()
    return (queryset)

def create_tarjeta_disponible(form):
    tarjeta = form.save(commit=False)

    inicio = time.time()
    tarjeta.descripcion = settings.F.encrypt(form.cleaned_data['descripcion'].encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando tarjeta disponible: {time.time() - inicio}")
    
    tarjeta.full_clean()
    tarjeta.save()
    return tarjeta