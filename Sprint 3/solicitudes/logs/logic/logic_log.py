from ..models import Log
from django.conf import settings
import time

def get_logs():
    queryset = Log.objects.all()
    return (queryset)

def create_log(form):
    log = form.save(commit=False)

    inicio = time.time()
    log.nombreEvento = settings.F.encrypt(form.cleaned_data['nombreEvento'].encode('utf-8')).decode('utf-8')
    log.direccionIP = settings.F.encrypt(form.cleaned_data['direccionIP'].encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando log: {time.time() - inicio}")

    log.full_clean()
    log.save()
    return log