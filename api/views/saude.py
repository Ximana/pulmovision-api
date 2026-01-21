from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import datetime


@api_view(['GET'])
def health_check(request):
    """Endpoint para verificar se a API está funcionando"""
    return Response({
        'status': 'ok',
        'servico': 'PulmoVision API',
        'versao': '1.0.0',
        'timestamp': datetime.datetime.now().isoformat(),
        'ambiente': 'desenvolvimento' if settings.DEBUG else 'producao'
    })
