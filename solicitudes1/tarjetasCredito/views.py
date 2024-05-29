from django.conf import settings
from django.shortcuts import render
import requests

from solicitudes.models import Solicitud
from .logic.logic_tarjetaCredito import create_tarjeta_credito, get_tarjetas_credito, get_tarjeta_credito_by_solicitud
from solicitudes.logic.logic_solicitud import getSolicitudById, update_solicitud

def tarjeta_list(request):
    cedula = request.GET.get('cedula')
    cliente = requests.get(settings.PATH_GET_CLIENTE, headers={"Accept":"application/json"}, params={'cedula': cedula}).json()
    solicitud = getSolicitudById(cliente["idSolicitud"])
    context = {
        'tarjeta': get_tarjeta_credito_by_solicitud(solicitud),
        'cedula': cedula
    }
    update_solicitud(solicitud, Solicitud.Etapa.ACTIVACION)
    return render(request, 'TarjetaCredito/activar.html', context)