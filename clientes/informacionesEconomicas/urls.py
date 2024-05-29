from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('informacionesEconomicas/', views.informacionEconomica_list),
    path('informacionEconomicaCreate/', csrf_exempt(views.informacionEconomica_create), name='informacionEconomicaCreate'),
]