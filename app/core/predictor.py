"""
Predictor - Lógica de Predição
Processa imagem e retorna diagnóstico
"""

import numpy as np
from PIL import Image
import io
import logging

from app.config import settings
from app.core.model_loader import get_model
from app.utils.image_processing import preprocess_image
from app.utils.exceptions import PredictionException

logger = logging.getLogger(__name__)


class Predictor:
    """Classe responsável por fazer predições em radiografias."""
    
    def __init__(self):
        self.model = None
        self.classes = settings.CLASSES
    
    def _load_model(self):
        """Carrega modelo (lazy loading)."""
        if self.model is None:
            self.model = get_model()
    
    def predict(self, image_data: bytes) -> dict:
        """
        Faz predição em uma radiografia.
        
        Args:
            image_data: Bytes da imagem
            
        Returns:
            dict: Resultado da predição com formato padrão
            
        Raises:
            PredictionException: Se houver erro na predição
        """
        try:
            # Carregar modelo
            self._load_model()
            
            # Preprocessar imagem
            logger.debug("Preprocessando imagem...")
            img_array = self._preprocess(image_data)
            
            # Fazer predição
            logger.debug("Executando predição...")
            predictions = self.model.predict(img_array, verbose=0)
            
            # Processar resultado
            result = self._format_result(predictions[0])
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na predição: {str(e)}", exc_info=True)
            raise PredictionException(f"Erro ao processar imagem: {str(e)}")
    
    def _preprocess(self, image_data: bytes) -> np.ndarray:
        """
        Preprocessa imagem para o modelo.
        
        Args:
            image_data: Bytes da imagem
            
        Returns:
            np.ndarray: Array preprocessado (1, 224, 224, 3)
        """
        try:
            # Abrir imagem
            img = Image.open(io.BytesIO(image_data))
            
            # Converter para RGB se necessário
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize para tamanho esperado
            img = img.resize((settings.IMAGE_SIZE, settings.IMAGE_SIZE), Image.BILINEAR)
            
            # Converter para array
            img_array = np.array(img, dtype=np.float32)
            
            # Normalizar (EfficientNet preprocessing)
            img_array = preprocess_image(img_array)
            
            # Adicionar dimensão de batch
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise PredictionException(f"Erro no preprocessamento: {str(e)}")
    
    def _format_result(self, predictions: np.ndarray) -> dict:
        """
        Formata resultado da predição.
        
        Args:
            predictions: Array de probabilidades (3,)
            
        Returns:
            dict: Resultado formatado
        """
        # Índice da classe com maior probabilidade
        predicted_idx = int(np.argmax(predictions))
        predicted_class = self.classes[predicted_idx]
        confidence = float(predictions[predicted_idx])
        
        # Probabilidades de todas as classes
        probabilities = {
            classe: float(predictions[i])
            for i, classe in enumerate(self.classes)
        }
        
        # Ordenar probabilidades (maior para menor)
        probabilities = dict(
            sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        )
        
        # Construir resposta
        result = {
            "resultado": {
                "rotulo": predicted_class,
                "confianca": confidence
            },
            "probabilidades": probabilities,
            "modelo": {
                "nome": settings.MODEL_NAME,
                "arquitetura": settings.MODEL_ARCHITECTURE,
                "versao": settings.MODEL_VERSION
            },
            "aviso_legal": settings.DISCLAIMER
        }
        
        # Adicionar aviso se confiança baixa
        if confidence < 0.7:
            result["aviso_confianca"] = (
                "Confiança baixa (< 70%). Recomenda-se revisão por especialista."
            )
        
        # Adicionar interpretação clínica básica
        result["interpretacao"] = self._get_interpretation(predicted_class, confidence)
        
        return result
    
    def _get_interpretation(self, classe: str, confianca: float) -> str:
        """
        Gera interpretação clínica básica.
        
        Args:
            classe: Classe predita
            confianca: Nível de confiança
            
        Returns:
            str: Interpretação
        """
        interpretacoes = {
            "normal": "Radiografia sem achados patológicos evidentes.",
            "pneumonia": "Achados sugestivos de pneumonia. Correlacionar com clínica.",
            "tuberculose": "Achados compatíveis com tuberculose. Investigação adicional recomendada."
        }
        
        base = interpretacoes.get(classe, "Classificação não reconhecida.")
        
        if confianca >= 0.9:
            nivel = "Alta confiança na classificação."
        elif confianca >= 0.7:
            nivel = "Confiança moderada. Considerar contexto clínico."
        else:
            nivel = "Baixa confiança. Revisão por especialista recomendada."
        
        return f"{base} {nivel}"
    
    def predict_batch(self, images_data: list) -> list:
        """
        Predição em lote (futuro).
        
        Args:
            images_data: Lista de bytes de imagens
            
        Returns:
            list: Lista de resultados
        """
        self._load_model()
        
        results = []
        for img_data in images_data:
            try:
                result = self.predict(img_data)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        
        return results