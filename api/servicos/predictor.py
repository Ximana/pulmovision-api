import numpy as np
from modelos.carregador import CarregadorModelo
from api.utilitarios.constantes import CLASSES

class ServicoPredicao:
    """Serviço responsável por fazer predições com o modelo"""
    
    @classmethod
    def predizer(cls, imagem_processada):
        """
        Faz a predição usando o modelo carregado
        """
        modelo = CarregadorModelo.obter_modelo()
        
        if modelo is None:
            raise RuntimeError("Modelo não carregado")
        
        # Fazer predição
        predicao = modelo.predict(imagem_processada, verbose=0)
        
        # Extrair resultados
        idx_classe = int(np.argmax(predicao, axis=1)[0])
        confianca = float(predicao[0][idx_classe])
        
        # Montar resultado
        resultado = {
            'rotulo': CLASSES[idx_classe],
            'confianca': confianca,
            'probabilidades': {
                CLASSES[i]: float(predicao[0][i]) 
                for i in range(len(CLASSES))
            }
        }
        
        return resultado