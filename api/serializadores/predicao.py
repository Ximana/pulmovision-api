from rest_framework import serializers
from api.utilitarios.validadores import ValidadorImagem

class PredicaoSerializer(serializers.Serializer):
    """Validação do upload de imagem para predição"""
    file = serializers.ImageField(
        required=True,
        error_messages={
            'required': 'O arquivo de imagem é obrigatório',
            'invalid': 'Arquivo inválido. Envie uma imagem válida.'
        }
    )
    
    def validate_file(self, arquivo):
        """Validações customizadas da imagem"""
        ValidadorImagem.validar(arquivo)
        return arquivo
