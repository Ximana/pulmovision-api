from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'API PulmoVision'

    def ready(self):
        """Carrega o modelo ML na inicialização da aplicação"""
        from modelos.carregador import CarregadorModelo
        CarregadorModelo.carregar_modelo()