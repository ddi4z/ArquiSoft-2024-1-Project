from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('verificacionesOTP/', views.verificacionesOTP, name='verificacionesOTP'),
    path('validarOTP/', views.validarOTP, name='validarOTP'),
]