"""
Rota de Limitações do Sistema
Transparência sobre capacidades e restrições do modelo
"""

from fastapi import APIRouter
from typing import List

from app.config import settings
from app.schemas.common import LimitationsResponse

router = APIRouter()


@router.get("/limitations", response_model=LimitationsResponse)
async def get_limitations():
    """
    Limitações e restrições do sistema.
    
    Retorna informações transparentes sobre:
    - Limitações técnicas do modelo
    - Casos onde o modelo pode falhar
    - Recomendações de uso
    - Avisos importantes
    
    **Transparência é fundamental em aplicações médicas!**
    
    Este endpoint garante que usuários estejam cientes das
    capacidades e limitações do sistema antes de utilizá-lo.
    """
    
    return LimitationsResponse(
        limitacoes_tecnicas=[
            "Dataset de treino limitado (~6.500 imagens)",
            "Treinado principalmente em crianças (1-5 anos) - performance pode variar em adultos",
            "Resolução de entrada reduzida para 224x224 pixels (perda de detalhes finos)",
            "Não detecta outras doenças além de pneumonia e tuberculose",
            "Performance degradada em imagens de baixa qualidade",
            "Sensível a artefatos (marcadores, eletrodos, próteses)",
            "Não quantifica gravidade da doença",
            "Não localiza especificamente os achados radiológicos"
        ],
        
        limitacoes_clinicas=[
            "Não tem acesso ao contexto clínico do paciente",
            "Não considera história clínica, sintomas ou exames laboratoriais",
            "Dificuldade em casos com múltiplas patologias simultâneas",
            "Apresentações atípicas de doenças podem não ser reconhecidas",
            "Estágios iniciais de doenças podem passar despercebidos",
            "Não substitui avaliação de profissional de saúde qualificado"
        ],
        
        casos_desafiadores=[
            "Imagens com má qualidade técnica (sub/superexposição)",
            "Posicionamento inadequado do paciente",
            "Presença de dispositivos médicos (drenos, sondas, pacemakers)",
            "Comorbidades pulmonares pré-existentes",
            "Pacientes imunossuprimidos (apresentações atípicas)",
            "Crianças muito jovens ou idosos (extremos de idade)",
            "Equipamentos de raio-X muito diferentes do dataset"
        ],
        
        taxa_de_erro={
            "acuracia_geral": "89.7%",
            "taxa_erro_esperada": "~10%",
            "falsos_negativos": {
                "pneumonia": "~6% (42 em 696 casos)",
                "tuberculose": "~19% (20 em 108 casos)"
            },
            "falsos_positivos": {
                "pneumonia": "~5%",
                "tuberculose": "~25% entre predições de TB"
            },
            "confusao_entre_classes": "36 casos confundidos entre pneumonia e tuberculose"
        },
        
        vieses_conhecidos=[
            "Viés demográfico: majoritariamente asiáticos e norte-americanos",
            "Viés de idade: principalmente crianças de 1-5 anos",
            "Viés de equipamento: hospitais modernos e bem equipados",
            "Viés de gravidade: casos mais evidentes podem estar sobre-representados",
            "Viés geográfico: China e EUA predominantes no dataset"
        ],
        
        recomendacoes_uso=[
            "Use apenas como ferramenta de TRIAGEM e APOIO à decisão",
            "SEMPRE revise resultados com profissional qualificado",
            "Considere confiança da predição: < 70% requer atenção especial",
            "Não use como diagnóstico definitivo",
            "Valide em sua população antes de uso clínico",
            "Monitore performance continuamente",
            "Estabeleça protocolo de supervisão humana",
            "Documente casos de erro para melhoria contínua"
        ],
        
        aviso_legal=settings.DISCLAIMER,
        
        status_regulatorio={
            "aprovacao": "Nenhuma",
            "tipo": "Protótipo de pesquisa",
            "uso_clinico": "NÃO aprovado para uso clínico",
            "requer": [
                "Validação clínica prospectiva",
                "Aprovação por agências regulatórias (ANVISA, FDA, etc.)",
                "Certificação de software médico",
                "Estudos multicêntricos"
            ]
        },
        
        quando_nao_usar=[
            "Como único critério para decisão de tratamento",
            "Em populações não validadas",
            "Sem supervisão de profissional qualificado",
            "Para diagnóstico de outras doenças não treinadas",
            "Quando contexto clínico contradiz resultado",
            "Em emergências que requerem decisão imediata"
        ]
    )


@router.get("/limitations/summary")
async def get_limitations_summary():
    """
    Resumo executivo das limitações.
    
    Versão condensada das principais limitações para
    exibição rápida em interfaces.
    """
    return {
        "resumo": "Sistema de apoio à decisão - NÃO substitui avaliação médica",
        "principais_limitacoes": settings.SYSTEM_LIMITATIONS,
        "taxa_erro": "~10%",
        "uso_aprovado": "Apenas pesquisa e triagem com supervisão",
        "aviso": settings.DISCLAIMER
    }