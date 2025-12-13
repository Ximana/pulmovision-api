# ==================== app/utils/logging.py ====================
"""Configuração de logging"""
import logging
import sys
from app.config import settings

def setup_logging():
    """Configura logging estruturado."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Silenciar logs verbosos do TensorFlow
    logging.getLogger('tensorflow').setLevel(logging.ERROR)
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configurado")
