from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class ImagemInvalidaException(Exception):
    """Exceção para imagens inválidas"""
    pass


def manipulador_excecoes_customizado(exc, context):
    """
    Handler customizado para exceções da API.
    Garante que sempre retorna uma resposta JSON válida.
    """
    # Primeiro, tenta usar o handler padrão do DRF
    response = exception_handler(exc, context)
    
    if response is not None:
        # Handler padrão conseguiu processar
        return response
    
    # Se chegou aqui, é um erro não tratado pelo DRF
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    
    # Retornar resposta JSON genérica
    return Response(
        {
            'erro': 'Erro interno do servidor',
            'detalhes': str(exc) if hasattr(exc, '__str__') else 'Erro desconhecido'
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )