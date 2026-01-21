from PIL import Image
import numpy as np
from io import BytesIO
from tensorflow.keras.applications.efficientnet import preprocess_input
from api.utilitarios.excecoes import ImagemInvalidaException

class ProcessadorImagem:
    """Processa e prepara imagens para o modelo"""
    
    IMG_SIZE = (224, 224)
    
    @classmethod
    def processar(cls, arquivo):
        """
        Processa a imagem recebida e retorna array preparado para o modelo
        """
        try:
            # Abrir imagem
            imagem = Image.open(arquivo)
            
            # Converter para RGB
            if imagem.mode != 'RGB':
                imagem = imagem.convert('RGB')
            
            # Redimensionar
            imagem = imagem.resize(cls.IMG_SIZE)
            
            # Converter para array
            img_array = np.array(imagem)
            
            # Preprocessar com EfficientNet
            img_array = preprocess_input(img_array)
            
            # Adicionar dimensão batch
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise ImagemInvalidaException(f"Erro ao processar imagem: {str(e)}")
