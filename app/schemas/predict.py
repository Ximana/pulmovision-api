"""
Schemas de Predição
Modelos Pydantic para request/response de predição
"""

from pydantic import BaseModel, Field
from typing import Dict


class ResultadoSchema(BaseModel):
    """Resultado da predição."""
    rotulo: str = Field(
        ...,
        description="Classe predita",
        example="pneumonia"
    )
    confianca: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Nível de confiança da predição (0-1)",
        example=0.92
    )


class ModeloSchema(BaseModel):
    """Informações do modelo usado."""
    nome: str = Field(..., description="Nome do modelo", example="PulmoVision")
    arquitetura: str = Field(..., description="Arquitetura do modelo", example="EfficientNetB0")
    versao: str = Field(..., description="Versão do modelo", example="1.0.0")


class PredictResponse(BaseModel):
    """
    Resposta completa de predição.
    
    Formato padronizado para todas as predições.
    """
    resultado: ResultadoSchema = Field(..., description="Resultado da classificação")
    
    probabilidades: Dict[str, float] = Field(
        ...,
        description="Probabilidades de cada classe (ordenadas)",
        example={
            "tuberculose": 0.92,
            "pneumonia": 0.06,
            "normal": 0.02
        }
    )
    
    modelo: ModeloSchema = Field(..., description="Informações do modelo")
    
    aviso_legal: str = Field(
        ...,
        description="Disclaimer médico obrigatório"
    )
    
    aviso_confianca: str | None = Field(
        None,
        description="Aviso adicional se confiança for baixa"
    )
    
    interpretacao: str | None = Field(
        None,
        description="Interpretação clínica básica"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "resultado": {
                    "rotulo": "tuberculose",
                    "confianca": 0.92
                },
                "probabilidades": {
                    "tuberculose": 0.92,
                    "pneumonia": 0.06,
                    "normal": 0.02
                },
                "modelo": {
                    "nome": "PulmoVision",
                    "arquitetura": "EfficientNetB0",
                    "versao": "1.0.0"
                },
                "aviso_legal": "Este resultado destina-se exclusivamente a fins de pesquisa...",
                "interpretacao": "Achados compatíveis com tuberculose. Alta confiança na classificação."
            }
        }