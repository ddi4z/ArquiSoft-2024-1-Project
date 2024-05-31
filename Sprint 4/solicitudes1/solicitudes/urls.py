from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('solicitudes/', views.solicitud_list),
    path('solicitudCreate/', csrf_exempt(views.solicitud_create), name='solicitudCreate'),
    path('nuevaSolicitud/', views.nuevaSolicitud, name='nuevaSolicitud'),
    path('getSolicitudById/', views.getSolicitudPagare, name='getSolicitudById'),
    path('addPagare/', csrf_exempt(views.addPagare), name='addPagare'),
    path('updateSolicitud/', csrf_exempt(views.updateSolicitud), name='updateSolicitud'),
]