from rest_framework import serializers
from . import models

class SolicitudSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'fechaInicio', 'fechaUltimaModificacion', 'etapaActual', 'lugarSolicitud', 'pagare')
        model = models.Solicitud