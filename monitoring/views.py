from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def health_check(request):
    """Endpoint para health check del ALB"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'monitoring-app',
        'version': '1.0.0'
    })