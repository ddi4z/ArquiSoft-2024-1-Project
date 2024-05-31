import base64
import hashlib
import json
from django.shortcuts import render
import requests
from .forms import InformacionEconomicaForm
from clientes.views import get_cliente_by_cedula
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_informacionEconomica import create_informacionEconomica, get_informacionesEconomicas
from django.conf import settings
import hmac
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

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

    solicitudId = requests.get(settings.PATH_CREATE_SOLICITUD, headers={"Accept":"application/json"}).json()
    cliente.solicitud = solicitudId['solicitud']
    cliente.save()


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
        form = InformacionEconomicaForm(request.POST, instance=informacion_economica)

        if form.is_valid():
            inicio = time.time()
            hmac_recibido = request.POST.get('hmac')
            data = {}
            for key in form.cleaned_data:
                data[key] = form.cleaned_data[key]
            
            for key in ['profesion', 'actividadEconomica', 'empresa']:
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
                informacion_economica_data = form.cleaned_data
                informacion_economica = cliente.infoEconomica

                if informacion_economica:
                    for key, value in informacion_economica_data.items():
                        setattr(informacion_economica, key, value)
                    informacion_economica.save()
                    messages.success(request, '¡InformacionEconomica actualizada exitosamente!')
                else:
                    informacion_economica = create_informacionEconomica(form)
                    print(1)
                    print(2)
                    print(3)
                    print(4)
                    print(5)
                    print(informacion_economica)
                    cliente.infoEconomica = informacion_economica
                    cliente.save()
                    messages.success(request, '¡InformacionEconomica creada exitosamente!')
                return HttpResponseRedirect('/oferta' + f'?cedula={cliente.cedula}')
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


