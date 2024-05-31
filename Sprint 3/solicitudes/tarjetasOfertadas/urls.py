from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('confirmar/', views.tarjeta_list, name='confirmar'),
    path('oferta/', views.tarjetas_list, name='oferta'),
    path('tarjetasOfertadasCreate/', csrf_exempt(views.tarjetasOfertadas_create), name='tarjetasOfertadasCreate'),
]