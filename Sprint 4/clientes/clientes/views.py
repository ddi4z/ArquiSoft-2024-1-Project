import base64
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
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

def cliente_list(request):
    clientes = get_clientes()
    context = {
        'cliente_list': clientes
    }
    return render(request, 'Cliente/clientes.html', context)

def cliente_create(request):
    if request.method == 'POST':
        private_key_pem = """-----BEGIN RSA PRIVATE KEY-----
        MIICXQIBAAKBgQDlOJu6TyygqxfWT7eLtGDwajtNFOb9I5XRb6khyfD1Yt3YiCgQ
        WMNW649887VGJiGr/L5i2osbl8C9+WJTeucF+S76xFxdU6jE0NQ+Z+zEdhUTooNR
        aY5nZiu5PgDB0ED/ZKBUSLKL7eibMxZtMlUDHjm4gwQco1KRMDSmXSMkDwIDAQAB
        AoGAfY9LpnuWK5Bs50UVep5c93SJdUi82u7yMx4iHFMc/Z2hfenfYEzu+57fI4fv
        xTQ//5DbzRR/XKb8ulNv6+CHyPF31xk7YOBfkGI8qjLoq06V+FyBfDSwL8KbLyeH
        m7KUZnLNQbk8yGLzB3iYKkRHlmUanQGaNMIJziWOkN+N9dECQQD0ONYRNZeuM8zd
        8XJTSdcIX4a3gy3GGCJxOzv16XHxD03GW6UNLmfPwenKu+cdrQeaqEixrCejXdAF
        z/7+BSMpAkEA8EaSOeP5Xr3ZrbiKzi6TGMwHMvC7HdJxaBJbVRfApFrE0/mPwmP5
        rN7QwjrMY+0+AbXcm8mRQyQ1+IGEembsdwJBAN6az8Rv7QnD/YBvi52POIlRSSIM
        V7SwWvSK4WSMnGb1ZBbhgdg57DXaspcwHsFV7hByQ5BvMtIduHcT14ECfcECQATe
        aTgjFnqE/lQ22Rk0eGaYO80cc643BXVGafNfd9fcvwBMnk0iGX0XRsOozVt5Azil
        psLBYuApa66NcVHJpCECQQDTjI2AQhFc1yRnCU/YgDnSpJVm1nASoRUnU8Jfm3Oz
        uku7JUXcVpt08DFSceCEX9unCuMcT72rAQlLpdZir876
        -----END RSA PRIVATE KEY-----"""
        private_key = RSA.import_key(private_key_pem)
        cipher = PKCS1_v1_5.new(private_key)
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

            for key in ['cedula', 'celular', 'direccion']:
                encrypted_data = data[key]
                # Decodifica el dato cifrado en base64
                try:
                    decoded_data = base64.b64decode(encrypted_data)
                except Exception as e:
                    print(f"Error decoding base64: {e}")
                    continue

                # Desencripta el dato decodificado
                sentinel = get_random_bytes(16)
                try:
                    decrypted_data = cipher.decrypt(decoded_data, sentinel)
                    data[key] = decrypted_data.decode('utf-8')
                    form.cleaned_data[key] = data[key]
                    print(f"Decrypted data for key {key}: {data[key]}")
                except ValueError as e:
                    print(f"Error decrypting data for key {key}: {e}")
                    continue

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

def cliente_get_id_solicitud(request):
    cedula = request.GET.get('cedula')
    cliente = get_cliente_by_cedula(cedula)
    context = {
        'idSolicitud': cliente.solicitud,
    }
    return JsonResponse(context, safe=False)

def cliente_get_correo(request):
    cedula = request.GET.get('cedula')
    cliente = get_cliente_by_cedula(cedula)
    context = {
        'correo': cliente.correo,
    }
    return JsonResponse(context, safe=False)

def cliente_get_cedula_decrypted(request):
    cedula = request.GET.get('cedula')
    cliente = get_cliente_by_cedula(cedula)
    context = {
        'cedulaDecrypted': cliente.cedula_decrypted
    }
    return JsonResponse(context, safe=False)

