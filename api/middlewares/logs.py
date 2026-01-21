import logging
import time

logger = logging.getLogger(__name__)

class LogMiddleware:
    """Middleware para logging de requisições"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        inicio = time.time()
        
        # Processar requisição
        response = self.get_response(request)
        
        # Calcular tempo
        duracao = time.time() - inicio
        
        # Log
        logger.info(
            f"{request.method} {request.path} - "
            f"Status: {response.status_code} - "
            f"Tempo: {duracao:.2f}s"
        )
        
        return response
