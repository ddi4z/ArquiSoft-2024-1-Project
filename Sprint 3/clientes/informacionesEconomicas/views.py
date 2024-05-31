import hashlib
import json
from django.shortcuts import render
from .forms import InformacionEconomicaForm
from clientes.views import get_cliente_by_cedula
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_informacionEconomica import create_informacionEconomica, get_informacionesEconomicas
from django.conf import settings
import hmac
import time

def informacionEconomica_list(request):
    informacionesEconomicas = get_informacionesEconomicas()
    context = {
        'informacionEconomica_list': informacionesEconomicas
    }
    return render(request, 'InformacionEconomica/informacionesEconomicas.html', context)

def informacionEconomica_create(request):
    cedula = request.GET.get('cedula')
    cliente = get_cliente_by_cedula(cedula)
    informacion_economica = cliente.infoEconomica

    #TODO: CREAR SOLICITUD MICRO
    # if not cliente.solicitud:
    #     solicitud = create_solicitud()
    #     cliente.solicitud = solicitud
    #     cliente.save()

    if request.method == 'POST':
        form = InformacionEconomicaForm(request.POST, instance=informacion_economica)
        if form.is_valid():
            inicio = time.time()
            hmac_recibido = request.POST.get('hmac')
            data = {}
            for key in form.cleaned_data:
                data[key] = form.cleaned_data[key]

            # Se simula la alteración en tránsito de la información económica
            # data['patrimonio'] = 1000000
            message = json.dumps(data, ensure_ascii=False)
            secret_key = settings.SECRET_KEY.encode('utf-8')
            hmac_calculado = hmac.new(secret_key, msg=message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

            print("mensaje info economica: " + message)
            print("HMAC info economica recibido: " + hmac_recibido)
            print("HMAC info economica calculado: " + hmac_calculado)
            
            if hmac_recibido == hmac_calculado:
                print(f"Tiempo HMAC info economica: {time.time() - inicio}")
                informacion_economica_nueva = create_informacionEconomica(form, cliente.cedula)
                cliente.infoEconomica = informacion_economica_nueva

                if informacion_economica:
                    messages.success(request, '¡InformacionEconomica actualizada exitosamente!')
                else:
                    messages.success(request, '¡InformacionEconomica creada exitosamente!')
                return HttpResponseRedirect(reverse('oferta') + f'?cedula={cliente.cedula}')
            else:
                print("¡HMAC inválido! Por favor, verifica la integridad de los datos.")
                messages.error(request, '¡HMAC inválido! Por favor, verifica la integridad de los datos.')
        else:
            print(form.errors)
    else:
        form = InformacionEconomicaForm(instance=informacion_economica)

    context = {
        'form': form,
    }

    return render(request, 'InformacionEconomica/informacionEconomicaCreate.html', context)


