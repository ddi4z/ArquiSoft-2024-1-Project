import hashlib
import hmac
import json
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests

from solicitudes.models import Solicitud
from solicitudes.logic.logic_solicitud import update_solicitud, getSolicitudById
from solicitudTDC.logic.logic_solicitudTDC import init_globals
from .logic.logic_tarjetaOfertada import create_tarjeta_ofertada, get_tarjetas_ofertadas, get_tarjetas_ofertadas_by_solicitud, get_tarjeta_ofertada_by_id
from tarjetasCredito.logic.logic_tarjetaCredito import create_tarjeta_credito, get_tarjeta_credito_by_solicitud, get_tarjetas_credito
import time

def tarjetas_list(request):
    init_globals()
    cedula = request.GET.get('cedula')

    cliente = requests.get(settings.PATH_GET_CLIENTE, headers={"Accept":"application/json"}, params={'cedula': cedula}).json()
    solicitud = getSolicitudById(cliente["idSolicitud"])

    tarjetas = get_tarjetas_ofertadas_by_solicitud(solicitud)

    context = {
        'tarjetas_list': tarjetas,
        'cedula': cedula
    }

    update_solicitud(solicitud, Solicitud.Etapa.PRESENTACION_OFERTA)
    
    if request.method == 'POST':
        tarjeta = request.POST.get('tarjeta')

        inicio = time.time()
        hmac_recibido = request.POST.get('hmac')
        tarjeta = get_tarjeta_ofertada_by_id(tarjeta)
        secret_key = settings.SECRET_KEY.encode('utf-8')


        message = json.dumps({'tarjeta': tarjeta.id}, ensure_ascii=False)
        hmac_calculado = hmac.new(secret_key, msg=message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

        print("mensaje tarjeta: " + message)
        print("HMAC tarjeta recibido: " + hmac_recibido)
        print("HMAC tarjeta calculado: " + hmac_calculado)
        if hmac_recibido == hmac_calculado:
            print(f"Tiempo HMAC tarjeta: {time.time() - inicio}")
            try:
                print(tarjeta.tarjetaCredito)
            except:
                credito = create_tarjeta_credito(tarjeta)
                credito.tipoTarjeta = tarjeta
                credito.save()
                tarjeta.save()
            return HttpResponseRedirect(reverse('validacionLugar') + f'?cedula={cedula}')
    return render(request, 'TarjetaOfertada/oferta.html', context)


def tarjeta_list(request):
    cedula = request.GET.get('cedula')
    cliente = requests.get(settings.PATH_GET_CLIENTE, headers={"Accept":"application/json"}, params={'cedula': cedula}).json()
    solicitud = getSolicitudById(cliente["idSolicitud"])
    context = {
        'tarjeta': get_tarjeta_credito_by_solicitud(solicitud),
        'cedula': cedula
    }
    update_solicitud(solicitud, Solicitud.Etapa.CONFIRMACION)
    return render(request, 'TarjetaOfertada/confirmar.html', context)


def tarjetasOfertadas_create(request):
    if request.method == 'POST':
        create_tarjeta_ofertada(request)
        return render(request, 'TarjetaOfertada/confirmar.html')
    return render(request, 'TarjetaOfertada/oferta.html')