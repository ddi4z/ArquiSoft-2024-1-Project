from django.db import models
from django.conf import settings

class InformacionEconomica():
    # e
    profesion = str()
    # e
    actividadEconomica = str()
    # e
    empresa = str()
    # e futuro
    ingresos = int()
    # e futuro
    egresos = int()
    # e futuro
    deudas = int()
    # e futuro
    patrimonio = int()

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
    
    @staticmethod
    def from_mongo(dto):
        info = InformacionEconomica()
        info.profesion = dto.get('infoEconomica.profesion', '')
        info.actividadEconomica = dto.get('infoEconomica.actividadEconomica', '')
        info.empresa = dto.get('infoEconomica.empresa', '')
        info.ingresos = dto.get('infoEconomica.ingresos', 0)
        info.egresos = dto.get('infoEconomica.egresos', 0)
        info.deudas = dto.get('infoEconomica.deudas', 0)
        info.patrimonio = dto.get('infoEconomica.patrimonio', 0)
        return info
