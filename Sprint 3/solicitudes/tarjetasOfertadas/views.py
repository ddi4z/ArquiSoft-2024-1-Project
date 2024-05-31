import hashlib
import hmac
import json
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from solicitudes.models import Solicitud
from .logic.logic_tarjetaOfertada import create_tarjeta_ofertada, get_tarjetas_ofertadas, get_tarjetas_ofertadas_by_solicitud, get_tarjeta_ofertada_by_id
from tarjetasCredito.logic.logic_tarjetaCredito import create_tarjeta_credito, get_tarjeta_credito_by_solicitud, get_tarjetas_credito
import time

def tarjetas_list(request):
    cedula = request.GET.get('cedula')
    # TODO: OBTENER CLIENTE POR CEDULA Y ACTUALIZAR SOLICITUD
    # cliente = get_cliente_by_cedula(cedula)
    # tarjetas = get_tarjetas_ofertadas_by_solicitud(cliente.solicitud)

    # context = {
    #     'tarjetas_list': tarjetas,
    #     'cedula': cedula
    # }

    # cliente = get_cliente_by_cedula(cedula)
    # update_solicitud(cliente.solicitud, Solicitud.Etapa.PRESENTACION_OFERTA)
    
    # if request.method == 'POST':
    #     tarjeta = request.POST.get('tarjeta')

    #     inicio = time.time()
    #     hmac_recibido = request.POST.get('hmac')
    #     tarjeta = get_tarjeta_ofertada_by_id(tarjeta)
    #     secret_key = settings.SECRET_KEY.encode('utf-8')


    #     message = json.dumps({'tarjeta': tarjeta.id}, ensure_ascii=False)
    #     hmac_calculado = hmac.new(secret_key, msg=message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

    #     print("mensaje tarjeta: " + message)
    #     print("HMAC tarjeta recibido: " + hmac_recibido)
    #     print("HMAC tarjeta calculado: " + hmac_calculado)
    #     if hmac_recibido == hmac_calculado:
    #         print(f"Tiempo HMAC tarjeta: {time.time() - inicio}")
    #         try:
    #             print(tarjeta.tarjetaCredito)
    #         except:
    #             credito = create_tarjeta_credito(tarjeta)
    #             credito.tipoTarjeta = tarjeta
    #             credito.save()
    #             tarjeta.save()
    #         return HttpResponseRedirect(reverse('validacionLugar') + f'?cedula={cedula}')
    # return render(request, 'TarjetaOfertada/oferta.html', context)
    pass

def tarjeta_list(request):
    # TODO: OBTENER CLIENTE POR CEDULA Y ACTUALIZAR SOLICITUD
    # cedula = request.GET.get('cedula')
    # cliente = get_cliente_by_cedula(cedula)
    # context = {
    #     'tarjeta': get_tarjeta_credito_by_solicitud(cliente.solicitud),
    #     'cedula': cedula
    # }
    # update_solicitud(cliente.solicitud, Solicitud.Etapa.CONFIRMACION)
    # return render(request, 'TarjetaOfertada/confirmar.html', context)
    pass

def tarjetasOfertadas_create(request):
    if request.method == 'POST':
        create_tarjeta_ofertada(request)
        return render(request, 'TarjetaOfertada/confirmar.html')
    return render(request, 'TarjetaOfertada/oferta.html')