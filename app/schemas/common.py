# ==================== app/schemas/common.py ====================
"""Schemas comuns"""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    model_status: str
    model_loaded: bool
    memory_usage_percent: float
    memory_available_gb: float

class LimitationsResponse(BaseModel):
    limitacoes_tecnicas: List[str]
    limitacoes_clinicas: List[str]
    casos_desafiadores: List[str]
    taxa_de_erro: Dict
    vieses_conhecidos: List[str]
    recomendacoes_uso: List[str]
    aviso_legal: str
    status_regulatorio: Dict
    quando_nao_usar: List[str]