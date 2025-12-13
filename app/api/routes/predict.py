"""
Rota de Predição - Endpoint Principal
Recebe radiografia e retorna diagnóstico
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Annotated
import logging

from app.schemas.predict import PredictResponse
from app.core.predictor import Predictor
from app.core.validator import ImageValidator
from app.utils.exceptions import (
    InvalidImageException,
    ImageTooLargeException,
    PredictionException
)

router = APIRouter()
logger = logging.getLogger(__name__)

# Instanciar validador e preditor
validator = ImageValidator()
predictor = Predictor()


@router.post("/predict", response_model=PredictResponse)
async def predict(
    file: Annotated[UploadFile, File(description="Radiografia torácica (JPG, PNG)")]
):
    """
    **Endpoint Principal: Predição de Doenças Pulmonares**
    
    Analisa uma radiografia torácica e retorna o diagnóstico.
    
    ## Entrada
    - **file**: Imagem da radiografia (.jpg, .jpeg, .png)
    - Tamanho máximo: 10MB
    - Formato: RGB ou Grayscale
    
    ## Saída
    - **resultado**: Classe predita e confiança
    - **probabilidades**: Probabilidades de cada classe
    - **modelo**: Informações do modelo usado
    - **aviso_legal**: Disclaimer médico
    
    ## Classes Possíveis
    - `normal`: Pulmões saudáveis
    - `pneumonia`: Pneumonia detectada
    - `tuberculose`: Tuberculose detectada
    
    ## Códigos de Erro
    - `400`: Imagem inválida ou formato não suportado
    - `413`: Imagem muito grande (> 10MB)
    - `500`: Erro interno no processamento
    
    ## Exemplo de Uso
    ```python
    import requests
    
    url = "http://localhost:8000/predict"
    files = {"file": open("radiografia.jpg", "rb")}
    response = requests.post(url, files=files)
    print(response.json())
    ```
    """
    
    logger.info(f"Nova requisição de predição: {file.filename}")
    
    try:
        # 1. Validar imagem
        logger.debug("Validando imagem...")
        image_data = await file.read()
        validator.validate(image_data, file.filename)
        
        # 2. Fazer predição
        logger.debug("Processando predição...")
        result = predictor.predict(image_data)
        
        logger.info(
            f"Predição concluída: {result['resultado']['rotulo']} "
            f"(confiança: {result['resultado']['confianca']:.2%})"
        )
        
        return result
        
    except InvalidImageException as e:
        logger.warning(f"Imagem inválida: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except ImageTooLargeException as e:
        logger.warning(f"Imagem muito grande: {str(e)}")
        raise HTTPException(status_code=413, detail=str(e))
    
    except PredictionException as e:
        logger.error(f"Erro na predição: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar a imagem. Por favor, tente novamente."
        )
    
    finally:
        # Limpar arquivo da memória
        await file.close()


@router.post("/predict/batch")
async def predict_batch():
    """
    Predição em lote (múltiplas imagens).
    
    Endpoint futuro para processar várias radiografias de uma vez.
    Atualmente não implementado.
    """
    raise HTTPException(
        status_code=501,
        detail="Predição em lote não implementada ainda. Use /predict para imagens individuais."
    )