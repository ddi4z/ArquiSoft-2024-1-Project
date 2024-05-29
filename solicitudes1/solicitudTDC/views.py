from django.conf import settings
from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import requests

from .logic.logic_solicitudTDC import init_globals
from solicitudes.models import Solicitud
from solicitudes.logic.logic_solicitud import getSolicitudById, update_solicitud

def index(request):
    init_globals()
    return render(request, 'index.html')

def terminosCondiciones(request):
    return render(request, 'terminosCondiciones.html')

def validacionLugar(request):
    print("aaa")
    cedula = request.GET.get('cedula')
    cliente = requests.get(settings.PATH_GET_CLIENTE, headers={"Accept":"application/json"}, params={'cedula': cedula}).json()
    solicitud = getSolicitudById(cliente["idSolicitud"])
    update_solicitud(solicitud, Solicitud.Etapa.VALIDACION_LUGAR)
    cedulaDecrypted = requests.get(settings.PATH_GET_CEDULA, headers={"Accept":"application/json"}, params={'cedula': cedula}).json()
    if int(cedulaDecrypted["cedulaDecrypted"])%2 == 0:
        solicitud.lugarSolicitud = Solicitud.LugarSolicitud.SUCURSAL_BANCARIA
        return render(request, 'validacionLugar.html')
    solicitud.lugarSolicitud = Solicitud.LugarSolicitud.APLICACION
    solicitud.save()
    print(settings.PATH_FIRMA + cedula)
    return HttpResponseRedirect(reverse('firma') + cedula)

def health_check(request):
    return JsonResponse({'message': 'OK'}, status = 200)