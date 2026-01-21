from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from modelos.carregador import CarregadorModelo
from api.utilitarios.constantes import LIMITACOES_SISTEMA


class ModeloInfoView(APIView):
    """Retorna informações sobre o modelo"""
    
    def get(self, request):
        try:
            info = CarregadorModelo.obter_informacoes()
            return Response(info)
        except Exception as e:
            return Response(
                {'erro': f'Erro ao obter informações: {str(e)}'},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LimitacoesView(APIView):
    """Retorna limitações do sistema (transparência)"""
    
    def get(self, request):
        try:
            return Response({
                'limitacoes': LIMITACOES_SISTEMA,
                'aviso': 'Este sistema é uma ferramenta de apoio à decisão clínica, não substitui avaliação médica profissional.'
            })
        except Exception as e:
            return Response(
                {'erro': f'Erro ao obter limitações: {str(e)}'},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )