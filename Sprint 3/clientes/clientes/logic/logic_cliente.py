from ..models import Cliente
import os
from django.conf import settings
import hashlib
from pymongo import MongoClient
import time

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def get_clientes():
    client = MongoClient(settings.MONGO_CLI)
    db = client.solicitud_tdc_db
    clientes_collection = db['clientes']

    clientes = []
    clientes_db = clientes_collection.find({})
    clientes += [ Cliente.from_mongo(cliente) for cliente in clientes_db ]
    
    client.close()
    return clientes

def verify_cliente(form):
    try:
        validate_email(form.cleaned_data['correo'])
    except ValidationError:
        raise ValidationError('Correo no válido')

    cliente = Cliente()
    cliente.nombres = form.cleaned_data['nombres']
    cliente.apellidos = form.cleaned_data['apellidos']
    cliente.pais = form.cleaned_data['pais']
    cliente.ciudad = form.cleaned_data['ciudad']
    cliente.fechaNacimiento = form.cleaned_data['fechaNacimiento']

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
    return cliente

def create_cliente(form):
    clientePlano = form.save(commit=False)
    clientePlano.full_clean()
    cliente = verify_cliente(form)

    client = MongoClient(settings.MONGO_CLI)
    db = client.solicitud_tdc_db
    clientes_collection = db['clientes']

    clientes_collection.insert_one({
        'cedula': cliente.cedula,
        'cedulaHash': cliente.cedulaHash,
        'nombres': cliente.nombres,
        'apellidos': cliente.apellidos,
        'celular': cliente.celular,
        'celularHash': cliente.celularHash,
        'correo': cliente.correo,
        'correoHash': cliente.correoHash,
        'pais': cliente.pais,
        'ciudad': cliente.ciudad,
        'direccion': cliente.direccion,
        'fechaNacimiento': cliente.fechaNacimiento
    })

    client.close()

    # TODO: CREAR CARPETA CLIENTE
    # if not os.path.exists("documentosClientes/" + cliente.cedula_decrypted):
    #     os.mkdir("documentosClientes/" + cliente.cedula_decrypted, mode=0o755)
    return cliente

def get_cliente_by_cedula(cedula):
    client = MongoClient(settings.MONGO_CLI)
    db = client.solicitud_tdc_db
    clientes_collection = db['clientes']

    cliente = clientes_collection.find_one({'cedula': cedula})
    client.close()
    return Cliente.from_mongo(cliente) if cliente else None
