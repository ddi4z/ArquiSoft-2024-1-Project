from django.shortcuts import render

from .forms import PagareForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_pagare import create_pagare, get_pagares
from firmasDigitales.logic.logic_firmaDigital import create_firmaDigital, update_firmaDigital
import json
from django.http import JsonResponse


def pagare_list(request):
    pagares = get_pagares()
    context = {
        'pagare_list': pagares
    }
    return render(request, 'Pagare/pagares.html', context)

def pagare_create(request):
    if request.method == 'POST':
        form = PagareForm(request.POST)
        if form.is_valid():
            create_pagare(form)
            messages.add_message(request, messages.SUCCESS, 'Pagare create successful')
            return HttpResponseRedirect(reverse('pagareCreate'))
        else:
            print(form.errors)
    else:
        form = PagareForm()

    context = {
        'form': form,
    }

    return render(request, 'Pagare/pagareCreate.html', context)

def firma(request):
    cedula = request.GET.get('cedula')
    # TODO:  OBTENER CLIENTE POR CEDULA, ENVIAR ETAPA DE SOLICITUD (String en vez de enumeracion) Y HACER UPDATE SOLICITUD
    # cliente = get_cliente_by_cedula(cedula)
    # update_solicitud(cliente.solicitud, Solicitud.Etapa.FIRMA_DOCUMENTOS)
    # if not bool(cliente.solicitud.pagare):
    #     cliente.solicitud.pagare = create_pagare(cliente.solicitud)
    #     cliente.solicitud.save()
    # context = {
    #     'cedula': cedula,
    #     'correo': cliente.correo,
    #     'firma': False
    # }

    # if cliente.solicitud.pagare.firma != "None":
    #     context['firma'] = True

    # if request.method == 'POST':
    #     try:
    #         json_data = json.loads(request.body)
    #         if not bool(cliente.solicitud.pagare.firma):
    #             cliente.solicitud.pagare.firma = create_firmaDigital(json_data, cliente.solicitud.pagare)
    #             cliente.solicitud.pagare.save()

    #         else:
    #             update_firmaDigital(json_data, cliente.solicitud.pagare.firma)

    #         return JsonResponse({'message': 'Datos recibidos exitosamente.'})
    #     except json.JSONDecodeError as e:
    #         return JsonResponse({'error': 'Los datos no son JSON válido.'}, status=400)
    # return render(request, 'Pagare/firma.html', context)