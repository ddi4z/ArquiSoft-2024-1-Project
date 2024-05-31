from django.shortcuts import render

from .forms import SolicitudForm
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .logic.logic_solicitud import create_solicitud, get_solicitudes, getSolicitudById, update_solicitud

def solicitud_list(request):
    solicitudes = get_solicitudes()
    context = {
        'solicitud_list': solicitudes
    }
    return render(request, 'Solicitud/solicitudes.html', context)

def nuevaSolicitud(request):
    solicitud = create_solicitud()
    return JsonResponse({'solicitud': solicitud.id})

def getSolicitudPagare(request):
    id = request.GET.get('id')
    solicitud = getSolicitudById(id)
    context = {
        'pagare': solicitud.pagare,
        'id': id
    }
    return JsonResponse(context, safe=False)

def addPagare(request):
    id = request.GET.get('idSolicitud')
    solicitud = getSolicitudById(id)
    pagare = request.GET.get('pagare')
    solicitud.pagare = pagare
    solicitud.save()
    return JsonResponse({'pagare': solicitud.pagare})

def updateSolicitud(request):
    id = request.GET.get('idSolicitud')
    etapa = request.GET.get('etapa')
    solicitud = getSolicitudById(id)
    update_solicitud(solicitud, etapa)

    print(solicitud)
    return JsonResponse({'etapa': solicitud.etapaActual})

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