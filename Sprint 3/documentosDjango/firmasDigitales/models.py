from django.db import models
from django.conf import settings

class FirmaDigital(models.Model):
    fechaFirma = models.DateTimeField(auto_now_add=True)
    # e
    ruta = models.CharField(max_length=512)

    class Meta:
        verbose_name_plural = "firmas digitales"

    def __str__(self):
        return '{}'.format(self.id)
    
    @property
    def ruta_decrypted(self):
        return settings.F.decrypt(self.ruta.encode('utf-8')).decode('utf-8')

