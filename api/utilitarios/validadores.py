from api.utilitarios.constantes import MAX_FILE_SIZE, ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES
from api.utilitarios.excecoes import ImagemInvalidaException

class ValidadorImagem:
    """Valida arquivos de imagem enviados"""
    
    @staticmethod
    def validar(arquivo):
        """Valida tamanho, tipo e extensão da imagem"""
        
        # Validar tamanho
        if arquivo.size > MAX_FILE_SIZE:
            tamanho_mb = MAX_FILE_SIZE / (1024 * 1024)
            raise ImagemInvalidaException(
                f"Arquivo muito grande. Tamanho máximo: {tamanho_mb}MB"
            )
        
        # Validar tipo MIME
        if arquivo.content_type not in ALLOWED_MIME_TYPES:
            raise ImagemInvalidaException(
                f"Tipo de arquivo não permitido. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Validar extensão
        extensao = arquivo.name.split('.')[-1].lower()
        if extensao not in ALLOWED_EXTENSIONS:
            raise ImagemInvalidaException(
                f"Extensão não permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        return True