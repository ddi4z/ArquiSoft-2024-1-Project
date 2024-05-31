from ..models import InformacionEconomica
from django.conf import settings
from pymongo import MongoClient
import time

def get_informacionesEconomicas():
    client = MongoClient(settings.MONGO_CLI)
    db = client.solicitud_tdc_db
    clientes_collection = db['clientes']

    infos = []
    clientes_db = clientes_collection.find({})
    infos += [ InformacionEconomica.from_mongo(cliente) for cliente in clientes_db ]
    
    client.close()
    return infos

def verify_informacionEconomica(form):
    infoEconomica = InformacionEconomica()
    infoEconomica.ingresos = form.cleaned_data['ingresos']
    infoEconomica.egresos = form.cleaned_data['egresos']
    infoEconomica.deudas = form.cleaned_data['deudas']
    infoEconomica.patrimonio = form.cleaned_data['patrimonio']

    inicio = time.time()
    infoEconomica.profesion = settings.F.encrypt(form.cleaned_data['profesion'].encode('utf-8')).decode('utf-8')
    infoEconomica.actividadEconomica = settings.F.encrypt(form.cleaned_data['actividadEconomica'].encode('utf-8')).decode('utf-8')
    infoEconomica.empresa = settings.F.encrypt(form.cleaned_data['empresa'].encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando info: {time.time() - inicio}")
    return infoEconomica

def create_informacionEconomica(form, cedula):
    infoEconomicaPlano = form.save(commit=False)
    infoEconomicaPlano.full_clean()
    infoEconomica = verify_informacionEconomica(form)
    
    client = MongoClient(settings.MONGO_CLI)
    db = client.solicitud_tdc_db
    clientes_collection = db['clientes']

    clientes_collection.update_one({
        'cedula': cedula
    }, {
        '$set': {
            'infoEconomica': {
                'profesion': infoEconomica.profesion,
                'actividadEconomica': infoEconomica.actividadEconomica,
                'empresa': infoEconomica.empresa,
                'ingresos': infoEconomica.ingresos,
                'egresos': infoEconomica.egresos,
                'deudas': infoEconomica.deudas,
                'patrimonio': infoEconomica.patrimonio
            }
        }
    })
    return infoEconomica