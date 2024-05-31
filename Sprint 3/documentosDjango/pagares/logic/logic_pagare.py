from ..models import Pagare
from django.utils import timezone

def get_pagares():
    queryset = Pagare.objects.all()
    return (queryset)

def create_pagare(solicitudAsociada):
    # TODO: CONECTARSE CON LA SOLICITUD ASOCIADA
    pagare = Pagare()
    pagare.fechaExpedicion = timezone.now()
    pagare.solicitud = solicitudAsociada
    pagare.full_clean()
    pagare.save()
    return pagare