from django.conf import settings

# Classes do modelo
CLASSES = ['normal', 'pneumonia', 'tuberculose']


# Disclaimer médico
DISCLAIMER_MEDICO = (
    "Este resultado destina-se exclusivamente a fins de pesquisa e apoio à "
    "decisão clínica, não devendo ser utilizado como diagnóstico médico definitivo. "
    "Consulte sempre um profissional de saúde qualificado."
)

# Limitações do sistema
LIMITACOES_SISTEMA = [
    "O modelo foi treinado com um conjunto específico de dados e pode não generalizar para todas as populações",
    "Radiografias de baixa qualidade podem afetar a precisão",
    "O sistema não detecta outras doenças pulmonares além das classes treinadas",
    "Não substitui a avaliação de um radiologista profissional",
    "Recomenda-se sempre confirmação clínica e exames complementares"
]

# Validação de arquivos
MAX_FILE_SIZE = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024  # Converter para bytes
ALLOWED_EXTENSIONS = settings.ALLOWED_IMAGE_FORMATS
ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/jpg']