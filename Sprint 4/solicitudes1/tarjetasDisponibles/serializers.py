from rest_framework import serializers
from . import models

class TarjetaDisponibleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'perfil', 'franquicia', 'imagen', 'descripcion', 'tiempoVigenciaMeses')
        model = models.TarjetaDisponible