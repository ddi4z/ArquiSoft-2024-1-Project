from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_verificacionOTP import send_otp, check_otp
from clientes.logic.logic_cliente import get_cliente_by_cedula

def verificacionesOTP(request):
    context = {
        'info': ""
    }
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        cliente = get_cliente_by_cedula(cedula)
        if cliente:
            try:
                send_otp(cedula)
                return HttpResponseRedirect(reverse('validarOTP') + f'?cedula={cliente.cedula}')
            except:
                context['info'] = "No se pudo enviar el OTP"
        if context['info'] == "":
            context['info'] = "No se encontró un cliente con la cédula ingresada"
    return render(request, 'verificacionOTP/verificacionesOTP.html', context)

def validarOTP(request):
    cedula = request.GET.get('cedula')
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        otp = request.POST.get('otp')
        cliente = get_cliente_by_cedula(cedula)
        if cliente:
            try:
                status = check_otp(cedula, otp)
                if status == 'approved':
                    return HttpResponseRedirect(reverse('informacionEconomicaCreate') + f'?cedula={cedula}')
            except:
                return HttpResponseRedirect(reverse('validarOTP') + f'?cedula={cedula}')
    return render(request, 'verificacionOTP/validarOTP.html', {'cedula': cedula})