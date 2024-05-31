import datetime
import hashlib
import hmac
import json
from django.conf import settings
from django.shortcuts import render
from .forms import ClienteForm
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .logic.logic_cliente import create_cliente, get_clientes, get_cliente_by_cedula
import time

def cliente_list(request):
    clientes = get_clientes()
    context = {
        'cliente_list': clientes
    }
    return render(request, 'Cliente/clientes.html', context)

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            inicio = time.time()
            hmac_recibido = request.POST.get('hmac')

            data = {}
            for key in form.cleaned_data:
                if isinstance(form.cleaned_data[key], datetime.date):
                    data[key] = form.cleaned_data[key].strftime("%Y-%m-%d")
                else:
                    data[key] = form.cleaned_data[key]
            message = json.dumps(data, ensure_ascii=False)
            secret_key = settings.SECRET_KEY.encode('utf-8')

            hmac_calculado = hmac.new(secret_key, msg=message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

            print("mensaje cliente: " + message)
            print("HMAC cliente recibido: " + hmac_recibido)
            print("HMAC cliente calculado: " + hmac_calculado)
            if hmac_recibido == hmac_calculado:
                print(f"Tiempo HMAC cliente: {time.time() - inicio}")
                cliente = create_cliente(form)
                messages.add_message(request, messages.SUCCESS, 'Cliente create successful')
                return HttpResponseRedirect(reverse('informacionEconomicaCreate') + f'?cedula={cliente.cedula}')
        else:
            print(form.errors)
    else:
        form = ClienteForm()

    context = {
        'form': form,
    }
    return render(request, 'Cliente/clienteCreate.html', context)

def cliente_exists(request):
    cedula = request.GET.get('cedula')
    cliente = get_cliente_by_cedula(cedula)
    if cliente is not None:
        existe = True
    else:
        existe = False
    context = {
        'existe': existe
    }
    return JsonResponse(context, safe=False)

def cliente_get_cedula_decrypted(request):
    cedula = request.GET.get('cedula')
    cliente = get_cliente_by_cedula(cedula)
    context = {
        'cedulaDecrypted': cliente.cedula_decrypted
    }
    return JsonResponse(context, safe=False)

