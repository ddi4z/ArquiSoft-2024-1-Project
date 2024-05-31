import base64
import hashlib
import hmac
import json
from django.conf import settings
from django.shortcuts import render

from documentosValidados.models import DocumentoValidado
from .forms import DocumentoValidadoForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_documentoValidado import create_documentoValidado, get_documentosValidados, validarArchivo
import time

def documentoValidado_list(request):
    documentosValidados = get_documentosValidados()
    context = {
        'documentoValidado_list': documentosValidados
    }
    return render(request, 'DocumentoValidado/documentosValidados.html', context)

def documentoValidado_create(request):
    if request.method == 'POST':
        form = DocumentoValidadoForm(request.POST)
        if form.is_valid():
            create_documentoValidado(form)
            messages.add_message(request, messages.SUCCESS, 'DocumentoValidado create successful')
            return HttpResponseRedirect(reverse('documentoValidadoCreate'))
        else:
            print(form.errors)
    else:
        form = DocumentoValidadoForm()

    context = {
        'form': form,
    }
    return render(request, 'DocumentoValidado/documentoValidadoCreate.html', context)

def carga(request):
    cedula = request.GET.get('cedula')
    context = {
        'cedula': cedula
    }

    # TODO:  OBTENER CLIENTE POR CEDULA, ENVIAR ETAPA DE SOLICITUD (String en vez de enumeracion) Y HACER UPDATE SOLICITUD
    # cliente = get_cliente_by_cedula(cedula)
    # if request.method == 'POST':
        
    #     archivo1 = request.FILES['cedulaFrontal']
    #     archivo2 = request.FILES['cedulaPosterior']
    #     archivo3 = request.FILES['desprendiblePago1']
    #     archivo4 = request.FILES['desprendiblePago2']

    #     inicio = time.time()
    #     hmac_recibido = request.POST.get('hmac')

    #     data = {
    #         'cedulaFrontal': {
    #             'name': archivo1.name,
    #             'size': archivo1.size,
    #         },
    #         'cedulaPosterior': {
    #             'name': archivo2.name,
    #             'size': archivo2.size,
    #         },
    #         'desprendiblePago1': {
    #             'name': archivo3.name,
    #             'size': archivo3.size,
    #         },
    #         'desprendiblePago2': {
    #             'name': archivo4.name,
    #             'size': archivo4.size,
    #         }
    #     }
    #     message = json.dumps(data, ensure_ascii=False)
    #     secret_key = settings.SECRET_KEY.encode('utf-8')

    #     hmac_calculado = hmac.new(secret_key, msg=message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    #     print("mensaje carga archivos: " + message)
    #     print("HMAC carga archivos recibido: " + hmac_recibido)
    #     print("HMAC carga archivos calculado: " + hmac_calculado)
    #     print(f"Tiempo HMAC carga archivos: {time.time() - inicio}")
        
    #     # Se revisa que sean png y pesen menos de 10MB
    #     valido = True
    #     for archivo in [archivo1, archivo2, archivo3, archivo4]:
    #         valido = valido and validarArchivo(archivo)
    #     if valido and hmac_recibido == hmac_calculado:
    #         cliente.solicitud.cedulaFrontal = create_documentoValidado(1, DocumentoValidado.DescripcionConfiabilidad.CONFIABLE, DocumentoValidado.TipoDocumento.CEDULA_FRONTAL, archivo1, cliente.solicitud)
    #         cliente.solicitud.cedulaPosterior = create_documentoValidado(1, DocumentoValidado.DescripcionConfiabilidad.CONFIABLE, DocumentoValidado.TipoDocumento.CEDULA_POSTERIOR, archivo2, cliente.solicitud)
    #         desprendibles = [create_documentoValidado(1, DocumentoValidado.DescripcionConfiabilidad.CONFIABLE, DocumentoValidado.TipoDocumento.DESPRENDIBLE_PAGO, archivo3, cliente.solicitud),
    #                             create_documentoValidado(1, DocumentoValidado.DescripcionConfiabilidad.CONFIABLE, DocumentoValidado.TipoDocumento.DESPRENDIBLE_PAGO, archivo4, cliente.solicitud)]
    #         cliente.solicitud.desprendiblePago = desprendibles
    #         cliente.solicitud.save()
    #         return HttpResponseRedirect(reverse('confirmar') + f'?cedula={cliente.cedula}')
    # update_solicitud(cliente.solicitud, Solicitud.Etapa.CARGUE_DOCUMENTOS)
    return render(request, 'DocumentoValidado/carga.html', context)