from ..models import Cliente
import os
from django.conf import settings
import hashlib
import time

def get_clientes():
    queryset = Cliente.objects.all()
    return (queryset)

def create_cliente(form):
    print("pepe")
    print("pepe")
    print(form.cleaned_data)
    cliente = form.save(commit=False)
    cliente.full_clean()


    inicio = time.time()
    cliente.cedula = settings.F.encrypt(form.cleaned_data['cedula'].encode('utf-8')).decode('utf-8')
    cliente.celular = settings.F.encrypt(form.cleaned_data['celular'].encode('utf-8')).decode('utf-8')
    cliente.correo = settings.F.encrypt(form.cleaned_data['correo'].encode('utf-8')).decode('utf-8')
    cliente.direccion = settings.F.encrypt(form.cleaned_data['direccion'].encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando cliente: {time.time() - inicio}")
    
    inicio = time.time()
    cliente.cedulaHash = hashlib.sha256(form.cleaned_data['cedula'].encode('utf-8')).hexdigest()
    cliente.celularHash = hashlib.sha256(form.cleaned_data['celular'].encode('utf-8')).hexdigest()
    cliente.correoHash = hashlib.sha256(form.cleaned_data['correo'].encode('utf-8')).hexdigest()
    print(f"Tiempo hasheando cliente: {time.time() - inicio}")

    cliente.save()
    # TODO: CREAR CARPETA CLIENTE
    # if not os.path.exists("documentosClientes/" + cliente.cedula_decrypted):
    #     os.mkdir("documentosClientes/" + cliente.cedula_decrypted, mode=0o755)
    return cliente

def get_cliente_by_cedula(cedula):
    queryset = Cliente.objects.filter(cedula=cedula)
    return queryset.first()
