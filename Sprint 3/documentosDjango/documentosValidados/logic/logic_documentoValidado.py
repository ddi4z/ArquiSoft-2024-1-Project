from ..models import DocumentoValidado
import os
from django.conf import settings
import time

def get_documentosValidados():
    queryset = DocumentoValidado.objects.all()
    return (queryset)

def create_documentoValidado(score, descripcion,tipo,archivo, solicitud):
    documentoValidado = DocumentoValidado()
    documentoValidado.score = score
    documentoValidado.descripcion = descripcion
    documentoValidado.tipo = tipo

    #TODO: OBTENER SOLICITUD Y CEDULA DECRYPTED

    # if not os.path.exists(f'documentosClientes/{solicitud.cliente.cedula_decrypted}'):
    #     os.makedirs(f'documentosClientes/{solicitud.cliente.cedula_decrypted}')

    # nombre = "desprendiblePago1.png"
    # if tipo == DocumentoValidado.TipoDocumento.CEDULA_FRONTAL:
    #     nombre = "cedulaFrontal.png"
    # elif tipo == DocumentoValidado.TipoDocumento.CEDULA_POSTERIOR:
    #     nombre = "cedulaPosterior.png"

    # ruta = f'documentosClientes/{solicitud.cliente.cedula_decrypted}/{nombre}'
    # if not os.path.exists(ruta):
    #     with open(ruta, 'wb+') as destination:
    #         for chunk in archivo.chunks():
    #             destination.write(chunk)
    # else:
    #     nombre = "desprendiblePago2.png"
    #     ruta = f'documentosClientes/{solicitud.cliente.cedula_decrypted}/{nombre}'
    #     with open(ruta, 'wb+') as destination:
    #         for chunk in archivo.chunks():
    #             destination.write(chunk)

    # inicio = time.time()
    # documentoValidado.ruta = settings.F.encrypt(ruta.encode('utf-8')).decode('utf-8')
    # print(f"Tiempo encriptando documento: {time.time() - inicio}")
    
    documentoValidado.solicitud = solicitud
    documentoValidado.full_clean()
    documentoValidado.save()
    return documentoValidado

def validarArchivo(archivo):
    if archivo.content_type != 'image/png':
        return False
    if archivo.size > 10000000:
        return False
    return True