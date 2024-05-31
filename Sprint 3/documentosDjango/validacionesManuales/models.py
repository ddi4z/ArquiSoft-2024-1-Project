from django.db import models
from django.conf import settings

class ValidacionManual(models.Model):
    # e futuro
    aprobado = models.BooleanField()
    # e
    descripcion = models.CharField(max_length=512)
    fechaValidacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "validaciones manuales"

    def __str__(self):
        return '{}'.format(self.id)
    
    @property
    def descripcion_decrypted(self):
        return settings.F.decrypt(self.descripcion.encode('utf-8')).decode('utf-8')

