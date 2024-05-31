from ..models import ValidacionManual
from django.conf import settings
import time

def get_validaciones_manuales():
    queryset = ValidacionManual.objects.all()
    return (queryset)

def create_validacion_manual(form):
    validacion = form.save(commit=False)
    validacion.full_clean()

    inicio = time.time()
    validacion.descripcion = settings.F.encrypt(form.cleaned_data['descripcion'].encode('utf-8')).decode('utf-8')
    print(f"Tiempo encriptando validación: {time.time() - inicio}")
    
    validacion.save()
    return validacion

def get_cliente_by_id(id):
    queryset = ValidacionManual.objects.filter(id=id)
    return queryset.first()