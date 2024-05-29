from rest_framework import serializers
from . import models

class LogSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'nombreEvento', 'codigoHTTP', 'metodoHTTP', 'direccionIP', 'solicitud')
        model = models.Log