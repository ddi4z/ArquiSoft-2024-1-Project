from clientes.models import Cliente
import os
from twilio.rest import Client

account_sid = ""
auth_token = ""
verify_sid = ""
client = Client(account_sid, auth_token)

def send_otp(cedula,):
    usuario = Cliente.objects.filter(cedula=cedula).first()
    verified_number = "+57" + str(usuario.celular)
    verification = client.verify.v2.services(verify_sid).verifications.create(to=verified_number, channel="sms")
    print(verification.status)

def check_otp(cedula, otp_code):
    print(otp_code)
    usuario = Cliente.objects.filter(cedula=cedula).first()
    verified_number = "+57" + str(usuario.celular)
    verification_check = client.verify.v2.services(verify_sid).verification_checks.create(to=verified_number, code=otp_code)
    return verification_check.status
