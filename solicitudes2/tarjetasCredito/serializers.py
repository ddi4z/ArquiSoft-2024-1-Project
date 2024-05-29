from rest_framework import serializers
from . import models

class TarjetaCreditoSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'numero', 'numeroHash', 'activada', 'fechaAdquisicion', 'fechaVencimiento', 'solicitud', 'tipoTarjeta')
        model = models.TarjetaCredito