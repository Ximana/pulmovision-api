from api.utilitarios.constantes import DISCLAIMER_MEDICO
from modelos.carregador import CarregadorModelo  # ← ADICIONAR este import


class FormatadorResposta:
    """Formata respostas da API de forma padronizada"""
    
    @classmethod
    def formatar(cls, resultado_predicao):
        """
        Formata o resultado da predição no formato JSON esperado
        """
        # Obter informações do modelo carregado dinamicamente
        info_modelo = CarregadorModelo.obter_informacoes()
        
        # Construir objeto modelo para resposta
        modelo_info = {
            'nome': info_modelo.get('nome', 'PulmoVision'),
            'arquitetura': info_modelo.get('arquitetura', 'EfficientNetB0'),
            'versao': info_modelo.get('versao', '1.0')
        }
        
        return {
            'resultado': {
                'rotulo': resultado_predicao['rotulo'],
                'confianca': round(resultado_predicao['confianca'], 4)
            },
            'probabilidades': {
                classe: round(prob, 4)
                for classe, prob in resultado_predicao['probabilidades'].items()
            },
            'modelo': modelo_info,  # vem do info_modelo.json
            'aviso_legal': DISCLAIMER_MEDICO
        }