from django.shortcuts import render

from solicitudes.models import Solicitud
from .logic.logic_tarjetaCredito import create_tarjeta_credito, get_tarjetas_credito, get_tarjeta_credito_by_solicitud
from solicitudes.logic.logic_solicitud import update_solicitud

def tarjeta_list(request):
    cedula = request.GET.get('cedula')
    # TODO: OBTENER CLIENTE POR CEDULA Y ACTUALIZAR SOLICITUD
    # cliente = get_cliente_by_cedula(cedula)
    # context = {
    #     'tarjeta': get_tarjeta_credito_by_solicitud(cliente.solicitud),
    #     'cedula': cedula
    # }
    # update_solicitud(cliente.solicitud, Solicitud.Etapa.ACTIVACION)
    # return render(request, 'TarjetaCredito/activar.html', context)