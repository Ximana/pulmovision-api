"""
Configurações da API PulmoVision
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # API Metadata
    API_TITLE: str = "PulmoVision API"
    API_DESCRIPTION: str = (
        "API para detecção de doenças pulmonares em radiografias torácicas. "
        "Classifica imagens em: Normal, Pneumonia ou Tuberculose."
    )
    API_VERSION: str = "1.0.0"
    
    # API Configuration
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_DEBUG: bool = Field(default=False, env="API_DEBUG")
    ENVIRONMENT: str = Field(default="production", env="ENVIRONMENT")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["*"],
        env="CORS_ORIGINS"
    )
    
    # Modelo
    MODEL_PATH: str = Field(
        default="./app/models/modelo_pulmonares.keras",
        env="MODEL_PATH"
    )
    MODEL_NAME: str = Field(default="PulmoVision", env="MODEL_NAME")
    MODEL_VERSION: str = Field(default="1.0.0", env="MODEL_VERSION")
    MODEL_ARCHITECTURE: str = Field(default="EfficientNetB0", env="MODEL_ARCHITECTURE")
    
    # Classes
    CLASSES: List[str] = ["normal", "pneumonia", "tuberculose"]
    
    # Processamento de Imagem
    IMAGE_SIZE: int = Field(default=224, env="IMAGE_SIZE")
    MAX_IMAGE_SIZE_MB: int = Field(default=10, env="MAX_IMAGE_SIZE_MB")
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png"]
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Aviso Legal
    DISCLAIMER: str = (
        "Este resultado destina-se exclusivamente a fins de pesquisa e apoio à "
        "decisão clínica, não devendo ser utilizado como diagnóstico médico definitivo. "
        "A avaliação final deve sempre ser realizada por um profissional de saúde qualificado."
    )
    
    # Limitações do Sistema
    SYSTEM_LIMITATIONS: List[str] = [
        "Dataset de treino limitado (~6.500 imagens)",
        "Treinado principalmente em crianças (1-5 anos)",
        "Performance pode variar em adultos e idosos",
        "Não detecta outras doenças pulmonares além das 3 classes",
        "Requer imagens de boa qualidade (raio-X PA ou AP)",
        "Taxa de erro esperada: ~10%",
        "Falsos negativos críticos podem ocorrer (especialmente TB)",
        "Não substitui avaliação médica especializada"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global de configurações
settings = Settings()


# Validações
def validate_settings():
    """Valida configurações na inicialização."""
    
    # Verificar se modelo existe
    if not os.path.exists(settings.MODEL_PATH):
        raise FileNotFoundError(
            f"Modelo não encontrado em: {settings.MODEL_PATH}\n"
            f"Por favor, coloque o modelo treinado neste caminho."
        )
    
    # Verificar tamanho máximo de imagem
    if settings.MAX_IMAGE_SIZE_MB <= 0:
        raise ValueError("MAX_IMAGE_SIZE_MB deve ser maior que 0")
    
    # Verificar tamanho da imagem
    if settings.IMAGE_SIZE <= 0:
        raise ValueError("IMAGE_SIZE deve ser maior que 0")
    
    print("✓ Configurações validadas com sucesso")


if __name__ == "__main__":
    # Testar configurações
    validate_settings()
    print("\nConfigurações atuais:")
    print(f"API: {settings.API_HOST}:{settings.API_PORT}")
    print(f"Modelo: {settings.MODEL_PATH}")
    print(f"Debug: {settings.API_DEBUG}")