from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

def index(request):
    return render(request, 'index.html')

def terminosCondiciones(request):
    return render(request, 'terminosCondiciones.html')

def health_check(request):
    return JsonResponse({'message': 'OK'}, status = 200)