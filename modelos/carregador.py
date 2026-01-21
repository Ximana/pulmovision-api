import os
import json
from pathlib import Path
import tensorflow as tf
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CarregadorModelo:
    """Gerencia o carregamento automático do modelo ML mais recente"""
    
    _modelo = None
    _config = None
    _info_modelo = None
    _carregado = False
    _diretorio_modelo = None
    
    @classmethod
    def _obter_modelo_mais_recente(cls):
        """
        Encontra o diretório do modelo mais recente em modelos/saved_models/
        Retorna o caminho completo do diretório mais recente
        """
        # Usar BASE_DIR em vez de MODELO_PATH
        diretorio_base = Path(settings.BASE_DIR) / 'modelos' / 'saved_models'
        
        if not diretorio_base.exists():
            logger.error(f"Diretório de modelos não encontrado: {diretorio_base}")
            return None
        
        # Listar todos os subdiretórios
        subdiretorios = [d for d in diretorio_base.iterdir() if d.is_dir()]
        
        if not subdiretorios:
            logger.error("Nenhum modelo encontrado no diretório")
            return None
        
        # Ordenar por data de modificação (mais recente primeiro)
        subdiretorios.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        modelo_mais_recente = subdiretorios[0]
        logger.info(f"📂 Modelo mais recente identificado: {modelo_mais_recente.name}")
        
        return modelo_mais_recente
    
    @classmethod
    def _carregar_arquivos_modelo(cls, diretorio_modelo):
        """
        Carrega os 3 arquivos necessários do diretório do modelo:
        1. modelo.keras - Arquivo do modelo treinado
        2. config.json - Configurações do modelo (gerado no treinamento)
        3. info_modelo.json - Informações sobre o modelo
        """
        arquivos = {
            'modelo': diretorio_modelo / 'modelo.keras',
            'config': diretorio_modelo / 'config.json',
            'info': diretorio_modelo / 'info_modelo.json'
        }
        
        # Verificar se todos os arquivos existem
        arquivos_faltando = []
        for nome, caminho in arquivos.items():
            if not caminho.exists():
                arquivos_faltando.append(str(caminho))
        
        if arquivos_faltando:
            logger.error(f"❌ Arquivos não encontrados: {', '.join(arquivos_faltando)}")
            raise FileNotFoundError(f"Arquivos necessários não encontrados: {arquivos_faltando}")
        
        return arquivos
    
    @classmethod
    def carregar_modelo(cls):
        """Carrega o modelo mais recente na memória"""
        if cls._carregado:
            logger.info("✓ Modelo já carregado")
            return
        
        try:
            # 1. Identificar modelo mais recente
            diretorio_modelo = cls._obter_modelo_mais_recente()
            
            if diretorio_modelo is None:
                logger.warning("⚠️ Nenhum modelo disponível para carregar")
                return
            
            # 2. Obter caminhos dos arquivos
            arquivos = cls._carregar_arquivos_modelo(diretorio_modelo)
            
            # 3. Carregar modelo TensorFlow (.keras)
            logger.info(f"📥 Carregando modelo: {arquivos['modelo']}")
            cls._modelo = tf.keras.models.load_model(str(arquivos['modelo']))
            
            # 4. Carregar configuração (config.json do treinamento)
            logger.info(f"📥 Carregando configuração: {arquivos['config']}")
            with open(arquivos['config'], 'r', encoding='utf-8') as f:
                cls._config = json.load(f)
            
            # 5. Carregar informações do modelo (info_modelo.json)
            logger.info(f"📥 Carregando informações: {arquivos['info']}")
            with open(arquivos['info'], 'r', encoding='utf-8') as f:
                cls._info_modelo = json.load(f)
            
            # Guardar referência ao diretório usado
            cls._diretorio_modelo = diretorio_modelo
            cls._carregado = True
            
            logger.info(f"✅ Modelo carregado com sucesso!")
            logger.info(f"   📁 Diretório: {diretorio_modelo.name}")
            logger.info(f"   🏷️  Nome: {cls._info_modelo.get('nome', 'N/A')}")
            logger.info(f"   📊 Arquitetura: {cls._info_modelo.get('arquitetura', 'N/A')}")
            logger.info(f"   🔢 Versão: {cls._info_modelo.get('versao', 'N/A')}")
            
        except FileNotFoundError as e:
            logger.error(f"❌ Erro: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao ler arquivo JSON: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Erro ao carregar modelo: {str(e)}", exc_info=True)
    
    @classmethod
    def obter_modelo(cls):
        """Retorna o modelo carregado"""
        if not cls._carregado:
            cls.carregar_modelo()
        return cls._modelo
    
    @classmethod
    def obter_informacoes(cls):
        """
        Retorna informações sobre o modelo carregadas do info_modelo.json
        """
        if not cls._carregado:
            cls.carregar_modelo()
        
        if not cls._carregado or cls._info_modelo is None:
            return {
                'erro': 'Modelo não carregado',
                'carregado': False
            }
        
        # Retornar informações do arquivo info_modelo.json + dados adicionais
        informacoes = cls._info_modelo.copy()
        
        # Adicionar informações extras
        informacoes.update({
            'carregado': cls._carregado,
            'diretorio': cls._diretorio_modelo.name if cls._diretorio_modelo else None,
            'classes': cls._config.get('classes', []) if cls._config else [],
            'parametros_treinaveis': cls._modelo.count_params() if cls._modelo else 0,
            'img_height': cls._config.get('img_height', 224) if cls._config else 224,
            'img_width': cls._config.get('img_width', 224) if cls._config else 224,
        })
        
        return informacoes
    
    @classmethod
    def obter_config(cls):
        """Retorna a configuração do modelo (config.json)"""
        if not cls._carregado:
            cls.carregar_modelo()
        return cls._config