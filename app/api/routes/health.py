"""
Rotas de Health Check
Verifica se a API está funcionando corretamente
"""

from fastapi import APIRouter, Depends
from datetime import datetime
import psutil
import os

from app.config import settings
from app.schemas.common import HealthResponse
from app.core.model_loader import get_model

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check completo da API.
    
    Retorna informações sobre:
    - Status da API
    - Status do modelo
    - Uso de memória
    - Timestamp
    """
    
    # Verificar se modelo está carregado
    try:
        model = get_model()
        model_status = "loaded"
        model_loaded = True
    except Exception as e:
        model_status = f"error: {str(e)}"
        model_loaded = False
    
    # Obter informações de sistema
    memory = psutil.virtual_memory()
    
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        timestamp=datetime.utcnow(),
        version=settings.API_VERSION,
        model_status=model_status,
        model_loaded=model_loaded,
        memory_usage_percent=memory.percent,
        memory_available_gb=round(memory.available / (1024**3), 2)
    )


@router.get("/")
async def root_health():
    """
    Health check simples.
    
    Verifica se a API está respondendo.
    Útil para load balancers e monitoring.
    """
    return {
        "status": "ok",
        "service": "PulmoVision API",
        "version": settings.API_VERSION
    }