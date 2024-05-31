from ..models import Solicitud
from django.utils import timezone

def get_solicitudes():
    queryset = Solicitud.objects.all()
    return (queryset)

def create_solicitud():
    solicitud = Solicitud()
    fecha = timezone.now()
    solicitud.fechaInicio = fecha
    solicitud.fechaUltimaModificacion = fecha
    solicitud.etapaActual = Solicitud.Etapa.INFORMACION_ECONOMICA
    solicitud.lugarSolicitud = Solicitud.LugarSolicitud.APLICACION
    solicitud.full_clean()
    solicitud.save()
    return solicitud

def update_solicitud(solicitud, etapaPaso):
    if solicitud.etapaActual ==  Solicitud.Etapa.INFORMACION_ECONOMICA and etapaPaso == Solicitud.Etapa.PRESENTACION_OFERTA:
        solicitud.etapaActual = etapaPaso
        solicitud.fechaUltimaModificacion = timezone.now()
        solicitud.save()
    elif solicitud.etapaActual ==  Solicitud.Etapa.PRESENTACION_OFERTA and etapaPaso == Solicitud.Etapa.VALIDACION_LUGAR:
        solicitud.etapaActual = etapaPaso
        solicitud.fechaUltimaModificacion = timezone.now()
        solicitud.save()
    elif solicitud.etapaActual ==  Solicitud.Etapa.VALIDACION_LUGAR and etapaPaso == Solicitud.Etapa.FIRMA_DOCUMENTOS:
        solicitud.etapaActual = etapaPaso
        solicitud.fechaUltimaModificacion = timezone.now()
        solicitud.save()
    elif solicitud.etapaActual ==  Solicitud.Etapa.FIRMA_DOCUMENTOS and etapaPaso == Solicitud.Etapa.CARGUE_DOCUMENTOS:
        solicitud.etapaActual = etapaPaso
        solicitud.fechaUltimaModificacion = timezone.now()
        solicitud.save()
    elif solicitud.etapaActual ==  Solicitud.Etapa.CARGUE_DOCUMENTOS and etapaPaso == Solicitud.Etapa.CONFIRMACION:
        solicitud.etapaActual = etapaPaso
        solicitud.fechaUltimaModificacion = timezone.now()
        solicitud.save()
    elif solicitud.etapaActual ==  Solicitud.Etapa.CONFIRMACION and etapaPaso == Solicitud.Etapa.ACTIVACION:
        solicitud.etapaActual = etapaPaso
        solicitud.fechaUltimaModificacion = timezone.now()
        solicitud.save()

    return solicitud
