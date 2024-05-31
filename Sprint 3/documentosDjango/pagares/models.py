from django.db import models
from firmasDigitales.models import FirmaDigital
from django.conf import settings

class Pagare(models.Model):
    # e
    ruta = models.CharField(max_length=512, blank=True)
    fechaExpedicion = models.DateField(auto_now_add=True)
    firma = models.OneToOneField(FirmaDigital, null=True, blank=True, on_delete=models.CASCADE, related_name='pagare', related_query_name='pagare')

    def __str__(self):
        return '{}'.format(self.id)
    
    @property
    def ruta_decrypted(self):
        return settings.F.decrypt(self.ruta.encode('utf-8')).decode('utf-8')
