from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .logic.logic_solicitudTDC import init_globals
from solicitudes.models import Solicitud
from solicitudes.logic.logic_solicitud import update_solicitud

def index(request):
    init_globals()
    return render(request, 'index.html')

def terminosCondiciones(request):
    return render(request, 'terminosCondiciones.html')

def validacionLugar(request):
    """
    cedula = request.GET.get('cedula')
    cliente = get_cliente_by_cedula(cedula)
    update_solicitud(cliente.solicitud, Solicitud.Etapa.VALIDACION_LUGAR)
    if int(cliente.cedula_decrypted)%2 == 0:
        cliente.solicitud.lugarSolicitud = Solicitud.LugarSolicitud.SUCURSAL_BANCARIA
        return render(request, 'validacionLugar.html')
    cliente.solicitud.lugarSolicitud = Solicitud.LugarSolicitud.APLICACION
    cliente.solicitud.save()
    return HttpResponseRedirect(reverse('firma') + f'?cedula={cedula}')
    """
    return render(request, 'index.html')

def health_check(request):
    return JsonResponse({'message': 'OK'}, status = 200)