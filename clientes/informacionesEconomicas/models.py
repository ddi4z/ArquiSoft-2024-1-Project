from djongo import models
from django.conf import settings

class InformacionEconomica(models.Model):
    idNumerico = models.PositiveIntegerField()
    # e
    profesion = models.CharField(max_length=512)
    # e
    actividadEconomica = models.CharField(max_length=512)
    # e
    empresa = models.CharField(max_length=512)
    # e futuro
    ingresos = models.PositiveIntegerField()
    # e futuro
    egresos = models.PositiveIntegerField()
    # e futuro
    deudas = models.PositiveIntegerField()
    # e futuro
    patrimonio = models.PositiveIntegerField()

    _id = models.ObjectIdField( primary_key=True, default=None)
    class Meta:
        verbose_name_plural = "informaciones economicas"

    def __str__(self):
        return '{}'.format(self.profesion)
    
    @property
    def profesion_decrypted(self):
        return settings.F.decrypt(self.profesion.encode('utf-8')).decode('utf-8')
    
    @property
    def actividadEconomica_decrypted(self):
        return settings.F.decrypt(self.actividadEconomica.encode('utf-8')).decode('utf-8')
    
    @property
    def empresa_decrypted(self):
        return settings.F.decrypt(self.empresa.encode('utf-8')).decode('utf-8')
