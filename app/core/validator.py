"""
Image Validator - Validação de Imagens
Verifica se imagem é válida antes de processar
"""

from PIL import Image
import io
import logging

from app.config import settings
from app.utils.exceptions import InvalidImageException, ImageTooLargeException

logger = logging.getLogger(__name__)


class ImageValidator:
    """Valida imagens enviadas para predição."""
    
    def __init__(self):
        self.max_size_bytes = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
        self.min_dimension = 100  # pixels
        self.max_dimension = 5000  # pixels
    
    def validate(self, image_data: bytes, filename: str = None):
        """
        Valida imagem completa.
        
        Args:
            image_data: Bytes da imagem
            filename: Nome do arquivo (opcional)
            
        Raises:
            InvalidImageException: Se imagem for inválida
            ImageTooLargeException: Se imagem for muito grande
        """
        
        # 1. Validar tamanho
        self._validate_size(image_data)
        
        # 2. Validar extensão
        if filename:
            self._validate_extension(filename)
        
        # 3. Validar formato e integridade
        self._validate_format(image_data)
        
        # 4. Validar dimensões
        self._validate_dimensions(image_data)
        
        logger.debug("✓ Imagem validada com sucesso")
    
    def _validate_size(self, image_data: bytes):
        """Valida tamanho do arquivo."""
        size_mb = len(image_data) / (1024 * 1024)
        
        if len(image_data) > self.max_size_bytes:
            raise ImageTooLargeException(
                f"Imagem muito grande: {size_mb:.2f}MB. "
                f"Tamanho máximo: {settings.MAX_IMAGE_SIZE_MB}MB"
            )
        
        logger.debug(f"Tamanho da imagem: {size_mb:.2f}MB")
    
    def _validate_extension(self, filename: str):
        """Valida extensão do arquivo."""
        extension = filename.split('.')[-1].lower()
        
        if extension not in self.allowed_extensions:
            raise InvalidImageException(
                f"Formato não suportado: .{extension}. "
                f"Formatos aceitos: {', '.join(self.allowed_extensions)}"
            )
        
        logger.debug(f"Extensão válida: .{extension}")
    
    def _validate_format(self, image_data: bytes):
        """Valida formato e integridade da imagem."""
        try:
            img = Image.open(io.BytesIO(image_data))
            
            # Verificar formato
            if img.format.lower() not in ['jpeg', 'jpg', 'png']:
                raise InvalidImageException(
                    f"Formato de imagem não suportado: {img.format}"
                )
            
            # Verificar se imagem não está corrompida
            img.verify()
            
            logger.debug(f"Formato válido: {img.format}")
            
        except InvalidImageException:
            raise
        except Exception as e:
            raise InvalidImageException(f"Imagem corrompida ou inválida: {str(e)}")
    
    def _validate_dimensions(self, image_data: bytes):
        """Valida dimensões da imagem."""
        try:
            img = Image.open(io.BytesIO(image_data))
            width, height = img.size
            
            # Verificar dimensões mínimas
            if width < self.min_dimension or height < self.min_dimension:
                raise InvalidImageException(
                    f"Imagem muito pequena: {width}x{height}. "
                    f"Dimensão mínima: {self.min_dimension}x{self.min_dimension}"
                )
            
            # Verificar dimensões máximas
            if width > self.max_dimension or height > self.max_dimension:
                raise InvalidImageException(
                    f"Imagem muito grande: {width}x{height}. "
                    f"Dimensão máxima: {self.max_dimension}x{self.max_dimension}"
                )
            
            # Verificar aspect ratio
            aspect_ratio = width / height
            if aspect_ratio < 0.5 or aspect_ratio > 2.0:
                logger.warning(
                    f"Aspect ratio incomum: {aspect_ratio:.2f}. "
                    "Imagem pode não ser uma radiografia de tórax."
                )
            
            logger.debug(f"Dimensões válidas: {width}x{height}")
            
        except InvalidImageException:
            raise
        except Exception as e:
            raise InvalidImageException(f"Erro ao validar dimensões: {str(e)}")
    
    def is_likely_xray(self, image_data: bytes) -> bool:
        """
        Verifica heurísticas para identificar se é raio-X.
        
        Não é 100% preciso, apenas indicativo.
        
        Returns:
            bool: True se parecer raio-X
        """
        try:
            img = Image.open(io.BytesIO(image_data))
            
            # Converter para grayscale
            if img.mode != 'L':
                img = img.convert('L')
            
            # Calcular estatísticas
            import numpy as np
            img_array = np.array(img)
            
            mean_intensity = img_array.mean()
            std_intensity = img_array.std()
            
            # Raio-X geralmente tem:
            # - Intensidade média baixa-média (áreas escuras)
            # - Alto desvio padrão (contraste)
            
            is_xray = (
                50 < mean_intensity < 180 and
                std_intensity > 40
            )
            
            if not is_xray:
                logger.warning(
                    "Imagem pode não ser uma radiografia de tórax "
                    f"(mean: {mean_intensity:.1f}, std: {std_intensity:.1f})"
                )
            
            return is_xray
            
        except Exception as e:
            logger.debug(f"Não foi possível verificar se é raio-X: {str(e)}")
            return True  # Assume que é válido em caso de erro