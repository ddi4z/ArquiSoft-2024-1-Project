from django.shortcuts import render
from .forms import SolicitudForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_solicitud import create_solicitud, get_solicitudes

def solicitud_list(request):
    solicitudes = get_solicitudes()
    context = {
        'solicitud_list': solicitudes
    }
    return render(request, 'Solicitud/solicitudes.html', context)

def solicitud_create(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            create_solicitud(form)
            messages.add_message(request, messages.SUCCESS, 'Solicitud create successful')
            return HttpResponseRedirect(reverse('solicitudCreate'))
        else:
            print(form.errors)
    else:
        form = SolicitudForm()

    context = {
        'form': form,
    }
    return render(request, 'Solicitud/solicitudCreate.html', context)