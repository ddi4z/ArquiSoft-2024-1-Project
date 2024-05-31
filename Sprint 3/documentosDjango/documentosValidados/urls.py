from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('documentosValidados/', views.documentoValidado_list),
    path('carga/', views.carga),
    path('documentoValidadoCreate/', csrf_exempt(views.documentoValidado_create), name='documentoValidadoCreate'),
]