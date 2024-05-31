from rest_framework import serializers
from . import models

class TarjetaOfertadaSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'cupo', 'solicitud', 'tarjetaDisponible')
        model = models.TarjetaOfertada