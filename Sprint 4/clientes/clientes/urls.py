from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('clientes/', views.cliente_list),
    path('clienteCreate/', csrf_exempt(views.cliente_create), name='clienteCreate'),
    path('clienteExists/', csrf_exempt(views.cliente_exists), name='clienteExists'),
    path('solicitudPorCedula/', csrf_exempt(views.cliente_get_id_solicitud), name='solicitudPorCedula'),
    path('clienteCedulaDecrypted/', csrf_exempt(views.cliente_get_cedula_decrypted), name='clienteCedulaDecrypted'),
    path('correoPorCedula/', csrf_exempt(views.cliente_get_correo), name='correoPorCedula'),
]