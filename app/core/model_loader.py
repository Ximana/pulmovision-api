"""
Model Loader - Carregamento do Modelo
Singleton para carregar modelo uma única vez
"""

import tensorflow as tf
import logging
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

# Variável global para armazenar modelo (singleton)
_model = None
_model_loaded = False


def get_model() -> tf.keras.Model:
    """
    Obtém o modelo carregado (singleton).
    
    Carrega o modelo apenas uma vez e reutiliza nas próximas chamadas.
    Isso economiza memória e tempo de inicialização.
    
    Returns:
        tf.keras.Model: Modelo carregado
        
    Raises:
        FileNotFoundError: Se modelo não for encontrado
        Exception: Se houver erro ao carregar modelo
    """
    global _model, _model_loaded
    
    if _model_loaded:
        return _model
    
    logger.info("Carregando modelo...")
    logger.info(f"Caminho: {settings.MODEL_PATH}")
    
    # Verificar se arquivo existe
    model_path = Path(settings.MODEL_PATH)
    if not model_path.exists():
        error_msg = f"Modelo não encontrado em: {settings.MODEL_PATH}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    try:
        # Carregar modelo
        _model = tf.keras.models.load_model(
            settings.MODEL_PATH,
            compile=False  # Não precisa compilar para inferência
        )
        
        # Informações do modelo
        total_params = _model.count_params()
        model_size_mb = model_path.stat().st_size / (1024 * 1024)
        
        logger.info(f"✓ Modelo carregado com sucesso")
        logger.info(f"  Parâmetros: {total_params:,}")
        logger.info(f"  Tamanho: {model_size_mb:.2f} MB")
        logger.info(f"  Input shape: {_model.input_shape}")
        logger.info(f"  Output shape: {_model.output_shape}")
        
        _model_loaded = True
        return _model
        
    except Exception as e:
        error_msg = f"Erro ao carregar modelo: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise Exception(error_msg)


def reload_model():
    """
    Recarrega o modelo.
    
    Útil para atualizar o modelo em runtime sem reiniciar a API.
    """
    global _model, _model_loaded
    
    logger.info("Recarregando modelo...")
    _model = None
    _model_loaded = False
    
    return get_model()


def get_model_info() -> dict:
    """
    Obtém informações sobre o modelo.
    
    Returns:
        dict: Informações do modelo
    """
    model = get_model()
    
    return {
        "input_shape": str(model.input_shape),
        "output_shape": str(model.output_shape),
        "total_layers": len(model.layers),
        "total_params": model.count_params(),
        "trainable_params": sum([tf.size(w).numpy() for w in model.trainable_weights]),
        "non_trainable_params": sum([tf.size(w).numpy() for w in model.non_trainable_weights])
    }


def warm_up_model():
    """
    Aquece o modelo fazendo uma predição dummy.
    
    A primeira predição sempre é mais lenta.
    Fazer um warm-up acelera predições subsequentes.
    """
    import numpy as np
    
    logger.info("Aquecendo modelo (warm-up)...")
    
    try:
        model = get_model()
        
        # Criar imagem dummy
        dummy_input = np.random.rand(1, settings.IMAGE_SIZE, settings.IMAGE_SIZE, 3)
        dummy_input = dummy_input.astype(np.float32)
        
        # Fazer predição dummy
        _ = model.predict(dummy_input, verbose=0)
        
        logger.info("✓ Warm-up concluído")
        
    except Exception as e:
        logger.warning(f"Falha no warm-up: {str(e)}")


# Warm-up automático na inicialização
if __name__ != "__main__":
    try:
        warm_up_model()
    except:
        pass  # Falha silenciosa no warm-up