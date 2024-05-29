from ..models import InformacionEconomica
from django.conf import settings
import time

def get_informacionesEconomicas():
    queryset = InformacionEconomica.objects.all()
    return (queryset)

def create_informacionEconomica(form):
    # obtiene el siguiente idNumerico
    informacionesEconomicas = get_informacionesEconomicas()
    idNumerico = 1
    if informacionesEconomicas:
        idNumerico = informacionesEconomicas.last().idNumerico + 1

    informacionEconomica = form.save(commit=False)
    informacionEconomica.idNumerico = idNumerico

    inicio = time.time()
    informacionEconomica.profesion = settings.F.encrypt(form.cleaned_data['profesion'].encode('utf-8')).decode('utf-8')
    informacionEconomica.actividadEconomica = settings.F.encrypt(form.cleaned_data['actividadEconomica'].encode('utf-8')).decode('utf-8')
    informacionEconomica.empresa = settings.F.encrypt(form.cleaned_data['empresa'].encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando info: {time.time() - inicio}")

    informacionEconomica.full_clean()
    informacionEconomica.save()
    return informacionEconomica