from logs.models import Log
from django.conf import settings

class LoggingMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request is not None:
            response = self.get_response(request)
            Log.objects.create(
                nombreEvento = settings.F.encrypt(request.get_full_path().encode('utf-8')).decode('utf-8'),
                codigoHTTP = response.status_code,
                metodoHTTP = request.method,
                direccionIP = settings.F.encrypt(request.META.get('REMOTE_ADDR', 'Unknown').encode('utf-8')).decode('utf-8'),
            )
        return response