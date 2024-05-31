import datetime

from informacionesEconomicas.models import InformacionEconomica
from django.conf import settings

class Cliente():
    # e
    cedula = str()
    # h
    cedulaHash = str()
    nombres = str()
    apellidos = str()
    # e
    celular = str()
    # h
    celularHash = str()
    # e
    correo = str()
    # h
    correoHash = str()
    pais = str()
    ciudad = str()
    # e
    direccion = str()
    # e futuro
    fechaNacimiento = datetime.date()

    infoEconomica = InformacionEconomica()
    #solicitud = models.OneToOneField(Solicitud, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def cedula_decrypted(self):
        return settings.F.decrypt(self.cedula.encode('utf-8')).decode('utf-8')
    
    @property
    def celular_decrypted(self):
        return settings.F.decrypt(self.celular.encode('utf-8')).decode('utf-8')
    
    @property
    def correo_decrypted(self):
        return settings.F.decrypt(self.correo.encode('utf-8')).decode('utf-8')
    
    @property
    def direccion_decrypted(self):
        return settings.F.decrypt(self.direccion.encode('utf-8')).decode('utf-8')
    
    def __str__(self):
        return '{}'.format(self.cedula)
        
    @staticmethod
    def from_mongo(dto):
        cliente = Cliente()
        cliente.cedula = dto.get('cedula', '')
        cliente.nombres = dto.get('nombres', '')
        cliente.apellidos = dto.get('apellidos', '')
        cliente.celular = dto.get('celular', '')
        cliente.correo = dto.get('correo', '')
        cliente.pais = dto.get('pais', '')
        cliente.ciudad = dto.get('ciudad', '')
        cliente.direccion = dto.get('direccion', '')
        cliente.fechaNacimiento = dto.get('fechaNacimiento', '')
        return cliente

