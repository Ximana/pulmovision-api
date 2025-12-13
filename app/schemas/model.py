# ==================== app/schemas/model.py ====================
"""Schemas de informações do modelo"""
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

class ModelInfoResponse(BaseModel):
    modelo: Dict
    classes: Dict
    dataset: Dict
    performance: Dict
    treinamento: Dict