from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializadores.predicao import PredicaoSerializer
from api.servicos.processador_imagem import ProcessadorImagem
from api.servicos.predictor import ServicoPredicao
from api.servicos.formatador_resposta import FormatadorResposta
from api.utilitarios.excecoes import ImagemInvalidaException
import logging

logger = logging.getLogger(__name__)

class PredicaoView(APIView):
    """
    Endpoint principal para predição de doenças pulmonares
    """
    
    def post(self, request):
        """Recebe imagem e retorna diagnóstico"""
        try:
            # Validar dados recebidos
            serializer = PredicaoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            arquivo_imagem = serializer.validated_data['file']
            
            # Processar imagem
            logger.info(f"Processando imagem: {arquivo_imagem.name}")
            imagem_processada = ProcessadorImagem.processar(arquivo_imagem)
            
            # Fazer predição
            resultado_predicao = ServicoPredicao.predizer(imagem_processada)
            
            # Formatar resposta
            resposta = FormatadorResposta.formatar(resultado_predicao)
            
            logger.info(f"Predição concluída: {resposta['resultado']['rotulo']}")
            return Response(resposta, status=status.HTTP_200_OK)
            
        except ImagemInvalidaException as e:
            logger.warning(f"Imagem inválida: {str(e)}")
            return Response(
                {'erro': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Erro na predição: {str(e)}", exc_info=True)
            return Response(
                {'erro': 'Erro interno ao processar a imagem'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )