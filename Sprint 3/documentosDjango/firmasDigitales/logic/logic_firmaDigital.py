from firmasDigitales.models import FirmaDigital
from django.conf import settings
import time

def create_firmaDigital(data,pagare):
    firma = FirmaDigital()
    firma.fechaFirma = data['updated_at']

    inicio = time.time()
    firma.ruta = settings.F.encrypt(data['submission_url'].encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando firma: {time.time() - inicio}")

    firma.pagare = pagare
    firma.full_clean()
    firma.save()
    return firma

def update_firmaDigital(data,firma):
    firma.fechaFirma = data['updated_at']

    inicio = time.time()
    firma.ruta = settings.F.encrypt(data['submission_url'].encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando firma: {time.time() - inicio}")
    
    firma.save()
    return firma