# ==================== app/api/dependencies.py ====================
"""Dependências compartilhadas"""
from fastapi import Depends
from app.core.model_loader import get_model
from app.config import settings

def get_settings():
    return settings

def get_predictor_model():
    return get_model()