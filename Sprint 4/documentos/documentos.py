import datetime
import hashlib
import hmac
import os
import time
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from decouple import config
from sqlalchemy.orm import relationship, backref
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')

current_dir = os.path.abspath(os.path.dirname(__file__))

db_dir = os.path.join(current_dir, 'base')
db_file = os.path.join(db_dir, 'db.sqlite3')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


class FirmaDigital(db.Model):
    __tablename__ = 'firma_digital'
    id = db.Column(db.Integer, primary_key=True)
    fecha_firma = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ruta = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return f'<FirmaDigital {self.id}>'

    @property
    def ruta_decrypted(self):
        return decrypt(self.ruta.encode('utf-8')).decode('utf-8')

class Pagare(db.Model):
    __tablename__ = 'pagare'
    id = db.Column(db.Integer, primary_key=True)
    ruta = db.Column(db.String(512), nullable=True, default="")
    fecha_expedicion = db.Column(db.Date, default=datetime.datetime.now)
    firma_id = db.Column(db.Integer, db.ForeignKey('firma_digital.id'), nullable=True)
    firma = relationship('FirmaDigital', backref=backref('pagare', uselist=False))

class ValidacionManual(db.Model):
    __tablename__ = 'validacion_manual'
    id = db.Column(db.Integer, primary_key=True)
    aprobado = db.Column(db.Boolean, nullable=False)
    descripcion = db.Column(db.String(512), nullable=False)
    fecha_validacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<ValidacionManual {self.id}>'

    @property
    def descripcion_decrypted(self):
        return decrypt(self.descripcion.encode('utf-8')).decode('utf-8')

class DocumentoValidado(db.Model):
    __tablename__ = 'documento_validado'

    class TipoDocumento:
        CEDULA_FRONTAL = 'CEDULA_FRONTAL'
        CEDULA_POSTERIOR = 'CEDULA_POSTERIOR'
        DESPRENDIBLE_PAGO = 'DESPRENDIBLE_PAGO'
        choices = [CEDULA_FRONTAL, CEDULA_POSTERIOR, DESPRENDIBLE_PAGO]

    class DescripcionConfiabilidad:
        CONFIABLE = 'CONFIABLE'
        NO_CONFIABLE = 'NO_CONFIABLE'
        choices = [CONFIABLE, NO_CONFIABLE]

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(256), nullable=False)
    ruta = db.Column(db.String(512), nullable=False)
    score = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(256), nullable=False, default=DescripcionConfiabilidad.NO_CONFIABLE)
    fecha_autovalidacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    validacion_manual_id = db.Column(db.Integer, db.ForeignKey('validacion_manual.id'), nullable=True)
    validacion_manual = relationship('ValidacionManual', backref=backref('documento_validado', uselist=False))

    def __repr__(self):
        return f'<DocumentoValidado {self.id}>'

    @property
    def ruta_decrypted(self):
        return decrypt(self.ruta.encode('utf-8')).decode('utf-8')

def decrypt(encrypted_data):

    return encrypted_data 

""" @app.route('/firma/<cedula>', methods=['GET', 'POST'])
def firma(cedula):
    idSolicitud = requests.get(config('PATH_GET_IDSOLICITUD'), headers={"Accept":"application/json"}, params={'cedula': cedula}).json()
    solicitud = requests.get(config('PATH_GET_SOLICITUD'), headers={"Accept":"application/json"}, params={'id': idSolicitud}).json()

    return render_template('firma.html', cedula=cedula, correo="", firma=False) """

@app.route('/firma', defaults={'cedula': None}, methods=['GET', 'POST'])
@app.route('/firma/<cedula>', methods=['GET', 'POST'])
def firma(cedula):
    idSolicitud = requests.get('http://10.128.0.15:8080/solicitudPorCedula/', headers={"Accept":"application/json"}, params={'cedula': cedula}).json()
    solicitud = requests.get('http://10.128.0.16:8080/getSolicitudById/', headers={"Accept":"application/json"}, params={'id': idSolicitud["idSolicitud"]}).json()
    pagare = db.session.get(Pagare, solicitud["pagare"])
    requests.put('http://10.128.0.16:8080/updateSolicitud/', headers={"Accept":"application/json"}, params={'idSolicitud': idSolicitud["idSolicitud"], 'etapa': 'FIRMA_DOCUMENTOS'})

    if pagare == None:
        pagare = Pagare()
        db.session.add(pagare)
        db.session.commit()
        requests.put('http://10.128.0.16:8080/addPagare/', headers={"Accept":"application/json"}, params={'idSolicitud': solicitud["id"], 'pagare': pagare.id})
    correo = requests.get('http://10.128.0.15:8080/correoPorCedula/', headers={"Accept":"application/json"}, params={'cedula': cedula}).json()["correo"]
    if request.method == 'POST':
        try:
            json_data = json.loads(request.data)
            if not bool(pagare.firma):
                firma = FirmaDigital()
                firma.fechaFirma = json_data['updated_at']
                firma.ruta = json_data['submission_url']
                db.session.add(firma)
                db.session.commit()
                pagare.firma = firma
                pagare.ruta = json_data['submission_url']
                db.session.commit()
            else:
                firma = db.session.get(FirmaDigital, pagare.firma.id)
                firma.fechaFirma = json_data['updated_at']
                firma.ruta = json_data['submission_url']
                db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error al recibir los datos.'})
        return jsonify({'message': 'Datos recibidos exitosamente.'})
    

    return render_template('firma.html', cedula=cedula, correo=correo, firma=pagare.firma != None)


def validarArchivo(archivo):
    if archivo.content_type != 'image/png':
        return False
    if archivo.content_length > 10 * 1024 * 1024: 
        return False
    return True

def create_documentoValidado(score, descripcion, tipo, archivo, cedula, solicitud):
    """Crea y guarda un DocumentoValidado con encriptación y lo añade a la sesión de la base de datos."""
    documentoValidado = DocumentoValidado()
    documentoValidado.score = score
    documentoValidado.descripcion = descripcion
    documentoValidado.tipo = tipo

    ENCRYPT_KEY = b'KSKvNI30yZToLcvP7RrIIvoiQEzN84gDZDdMs6Bb7O4='
    F = Fernet(ENCRYPT_KEY)

    # Crear directorio si no existe
    cedula_dir = f'documentosClientes/{cedula}'
    if not os.path.exists(cedula_dir):
        os.makedirs(cedula_dir)

    # Determinar nombre del archivo
    if tipo == DocumentoValidado.TipoDocumento.CEDULA_FRONTAL:
        nombre = "cedulaFrontal.png"
    elif tipo == DocumentoValidado.TipoDocumento.CEDULA_POSTERIOR:
        nombre = "cedulaPosterior.png"
    elif tipo == DocumentoValidado.TipoDocumento.DESPRENDIBLE_PAGO:
        nombre = "desprendiblePago1.png"
        # Si ya existe un desprendible de pago, se guarda con otro nombre
        if os.path.exists(os.path.join(cedula_dir, nombre)):
            nombre = "desprendiblePago2.png"


    ruta = os.path.join(cedula_dir, nombre)

    # Guardar archivo
    with open(ruta, 'wb') as destination:
        archivo.seek(0)
        for chunk in archivo.stream:
            destination.write(chunk)

    # Encriptar la ruta del archivo
    inicio = time.time()
    documentoValidado.ruta = F.encrypt(ruta.encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando documento: {time.time() - inicio}")

    documentoValidado.solicitud = solicitud
    db.session.add(documentoValidado)
    db.session.commit()
    return documentoValidado

@app.route('/documentosValidados/', methods=['GET', 'POST'])
def documentosValidados_list():
    documentos = DocumentoValidado.query.all()
    return render_template('documentosValidados.html', documento_list=documentos)

@app.route('/carga', defaults={'cedula': None}, methods=['GET', 'POST'])
@app.route('/carga/<cedula>', methods=['GET', 'POST'])
def carga(cedula):
    try:
        idSolicitud = requests.get('http://10.128.0.15:8080/solicitudPorCedula/', headers={"Accept": "application/json"}, params={'cedula': cedula}).json()
        requests.put('http://10.128.0.16:8080/updateSolicitud/', headers={"Accept": "application/json"}, params={'idSolicitud': idSolicitud["idSolicitud"], 'etapa': 'CARGUE_DOCUMENTOS'})
    except requests.RequestException as e:
        return f"Error en la solicitud: {e}", 500

    if request.method == 'POST':
        archivo1 = request.files['cedulaFrontal']
        archivo2 = request.files['cedulaPosterior']
        archivo3 = request.files['desprendiblePago1']
        archivo4 = request.files['desprendiblePago2']

        inicio = time.time()
        hmac_recibido = request.form.get('hmac')

        data = {
            'cedulaFrontal': {
                'name': archivo1.filename,
                'size': len(archivo1.read()),
            },
            'cedulaPosterior': {
                'name': archivo2.filename,
                'size': len(archivo2.read()),
            },
            'desprendiblePago1': {
                'name': archivo3.filename,
                'size': len(archivo3.read()),
            },
            'desprendiblePago2': {
                'name': archivo4.filename,
                'size': len(archivo4.read()),
            }
        }

        archivo1.seek(0)
        archivo2.seek(0)
        archivo3.seek(0)
        archivo4.seek(0)

        message = json.dumps(data, ensure_ascii=False).encode('utf-8')
        secret_key = b'django-insecure-%hli0)=#odc5pd_xqtyaktwh#y_&(7o$566y&b=a&vkr=oz19p'

        hmac_calculado = hmac.new(secret_key, msg=message, digestmod=hashlib.sha256).hexdigest()
        print("mensaje carga archivos: " + message.decode('utf-8'))
        print("HMAC carga archivos recibido: " + hmac_recibido)
        print("HMAC carga archivos calculado: " + hmac_calculado)
        print(f"Tiempo HMAC carga archivos: {time.time() - inicio}")

        valido = all([validarArchivo(archivo) for archivo in [archivo1, archivo2, archivo3, archivo4]])

        try:
            cedulaDecrypted = requests.get('http://10.128.0.15:8080/clienteCedulaDecrypted/', headers={"Accept": "application/json"}, params={'cedula': cedula}).json()["cedulaDecrypted"]
        except requests.RequestException as e:
            return f"Error en la solicitud de cedula: {e}", 500

        if valido and hmac_recibido == hmac_calculado:
            create_documentoValidado(1, DocumentoValidado.DescripcionConfiabilidad.CONFIABLE, DocumentoValidado.TipoDocumento.CEDULA_FRONTAL, archivo1, cedulaDecrypted, idSolicitud["idSolicitud"])
            create_documentoValidado(1, DocumentoValidado.DescripcionConfiabilidad.CONFIABLE, DocumentoValidado.TipoDocumento.CEDULA_POSTERIOR, archivo2, cedulaDecrypted, idSolicitud["idSolicitud"])
            desprendibles = [
                create_documentoValidado(1, DocumentoValidado.DescripcionConfiabilidad.CONFIABLE, DocumentoValidado.TipoDocumento.DESPRENDIBLE_PAGO, archivo3, cedulaDecrypted, idSolicitud["idSolicitud"]),
                create_documentoValidado(1, DocumentoValidado.DescripcionConfiabilidad.CONFIABLE, DocumentoValidado.TipoDocumento.DESPRENDIBLE_PAGO, archivo4, cedulaDecrypted, idSolicitud["idSolicitud"])
            ]
            db.session.commit()
            return redirect('/confirmar/?cedula=' + cedula)

    return render_template('carga.html', cedula=cedula)

@app.route('/pagares/', methods=['GET', 'POST'])
def pagares_list():
    pagares = Pagare.query.all()
    return render_template('pagares.html', pagare_list=pagares)

@app.route('/firmas/', methods=['GET', 'POST'])
def firmas_list():
    firmas = FirmaDigital.query.all()
    return render_template('firmas.html', firma_list=firmas)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
