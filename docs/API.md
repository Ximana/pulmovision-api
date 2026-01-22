# Documentação da API PulmoVision

**Versão:** 1.0  
**Última Atualização:** 16 de Dezembro de 2025

---

## Sumário

- [Visão Geral](#visão-geral)
- [URL Base](#url-base)
- [Autenticação](#autenticação)
- [Endpoints](#endpoints)
  - [Health Check](#1-health-check)
  - [Predição de Radiografia](#2-predição-de-radiografia)
  - [Informações do Modelo](#3-informações-do-modelo)
  - [Limitações do Sistema](#4-limitações-do-sistema)
- [Códigos de Resposta HTTP](#códigos-de-resposta-http)
- [Tratamento de Erros](#tratamento-de-erros)
- [Exemplos de Uso](#exemplos-de-uso)
- [Limitações e Considerações](#limitações-e-considerações)

---

## Visão Geral

A **API PulmoVision** é um serviço REST para detecção automatizada de doenças pulmonares (pneumonia e tuberculose) em radiografias torácicas utilizando Deep Learning. O sistema é baseado em EfficientNetB0 e fornece predições com níveis de confiança para auxiliar profissionais de saúde no diagnóstico.

### Características Principais

- ✅ Detecção de 3 classes: **normal**, **pneumonia**, **tuberculose**
- ✅ API RESTful stateless (sem banco de dados)
- ✅ Respostas em formato JSON
- ✅ Validação rigorosa de imagens
- ✅ Disclaimer médico automático em todas as respostas
- ✅ Carregamento automático do modelo mais recente
- ✅ Logging completo de requisições

### Casos de Uso

- Triagem inicial de radiografias torácicas
- Apoio à decisão clínica
- Pesquisa e desenvolvimento em diagnóstico por imagem
- Fins educacionais e de treinamento

---

## URL Base

### Desenvolvimento
```
http://localhost:8000
```

### Produção
```
https://api.pulmovision.com
```

---

## Autenticação

**Versão Atual:** Sem autenticação (API pública para desenvolvimento)

**Versão Futura:** Planejado suporte para:
- Token Bearer
- API Keys
- OAuth 2.0

---

## Endpoints

### 1. Health Check

Verifica se a API está funcionando e retorna informações básicas do serviço.

#### **Request**

```http
GET /health
```

#### **Parâmetros**

Nenhum parâmetro necessário.

#### **Resposta de Sucesso (200 OK)**

```json
{
  "status": "ok",
  "servico": "PulmoVision API",
  "versao": "1.0.0",
  "timestamp": "2025-12-16T10:30:45.123456",
  "ambiente": "desenvolvimento"
}
```

#### **Campos da Resposta**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `status` | string | Status da API (`ok` ou `erro`) |
| `servico` | string | Nome do serviço |
| `versao` | string | Versão da API |
| `timestamp` | string | Timestamp ISO 8601 da resposta |
| `ambiente` | string | Ambiente de execução (`desenvolvimento` ou `producao`) |

#### **Exemplos de Uso**

**cURL:**
```bash
curl http://localhost:8000/health
```

**Python:**
```python
import requests

response = requests.get('http://localhost:8000/health')
data = response.json()
print(f"Status: {data['status']}")
```

**JavaScript:**
```javascript
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log('Status:', data.status));
```

---

### 2. Predição de Radiografia

**Endpoint principal** da API. Analisa uma radiografia torácica e retorna o diagnóstico com probabilidades.

#### **Request**

```http
POST /predicao
Content-Type: multipart/form-data
```

#### **Parâmetros**

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `file` | File | Sim | Arquivo da radiografia torácica |

#### **Validações de Arquivo**

- **Formatos aceitos:** `.jpg`, `.jpeg`, `.png`
- **Tamanho máximo:** 10 MB
- **Tipo MIME aceito:** `image/jpeg`, `image/png`
- **Dimensões:** Redimensionadas automaticamente para 224x224 pixels

#### **Resposta de Sucesso (200 OK)**

```json
{
  "resultado": {
    "rotulo": "tuberculose",
    "confianca": 0.9234
  },
  "probabilidades": {
    "tuberculose": 0.9234,
    "pneumonia": 0.0612,
    "normal": 0.0154
  },
  "modelo": {
    "nome": "PulmoVision ChestXRay v2",
    "arquitetura": "EfficientNetB0",
    "versao": "2.0"
  },
  "aviso_legal": "Este resultado destina-se exclusivamente a fins de pesquisa e apoio à decisão clínica, não devendo ser utilizado como diagnóstico médico definitivo. Consulte sempre um profissional de saúde qualificado."
}
```

#### **Campos da Resposta**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `resultado.rotulo` | string | Classe prevista (`normal`, `pneumonia`, `tuberculose`) |
| `resultado.confianca` | float | Nível de confiança da predição (0.0 a 1.0) |
| `probabilidades` | object | Probabilidades para cada classe |
| `modelo.nome` | string | Nome do modelo utilizado |
| `modelo.arquitetura` | string | Arquitetura do modelo |
| `modelo.versao` | string | Versão do modelo |
| `aviso_legal` | string | Disclaimer médico obrigatório |

#### **Possíveis Rótulos**

| Rótulo | Descrição |
|--------|-----------|
| `normal` | Radiografia sem anormalidades detectadas |
| `pneumonia` | Pneumonia detectada |
| `tuberculose` | Tuberculose detectada |

#### **Resposta de Erro (400 Bad Request)**

```json
{
  "erro": "Arquivo muito grande. Tamanho máximo: 10.0MB"
}
```

**Possíveis Mensagens de Erro:**

- `"O arquivo de imagem é obrigatório"`
- `"Arquivo muito grande. Tamanho máximo: 10.0MB"`
- `"Tipo de arquivo não permitido. Use: jpg, jpeg, png"`
- `"Extensão não permitida. Use: jpg, jpeg, png"`

#### **Resposta de Erro (500 Internal Server Error)**

```json
{
  "erro": "Erro interno ao processar a imagem"
}
```

#### **Exemplos de Uso**

**cURL (Linux/Mac):**
```bash
curl -X POST http://localhost:8000/predicao \
  -F "file=@radiografia.jpg"
```

**cURL (Windows PowerShell):**
```powershell
curl.exe -X POST http://localhost:8000/predicao `
  -F "file=@C:\caminho\radiografia.jpg"
```

**Python:**
```python
import requests

url = 'http://localhost:8000/predicao'
files = {'file': open('radiografia.jpg', 'rb')}

response = requests.post(url, files=files)
resultado = response.json()

print(f"Diagnóstico: {resultado['resultado']['rotulo']}")
print(f"Confiança: {resultado['resultado']['confianca']:.2%}")
print(f"\nProbabilidades:")
for classe, prob in resultado['probabilidades'].items():
    print(f"  {classe}: {prob:.2%}")
```

**JavaScript (FormData):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/predicao', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Diagnóstico:', data.resultado.rotulo);
  console.log('Confiança:', data.resultado.confianca);
  console.log('Probabilidades:', data.probabilidades);
});
```

**Postman:**
1. Método: `POST`
2. URL: `http://localhost:8000/predicao`
3. Body → `form-data`
4. Key: `file` (tipo: File)
5. Value: Selecione a imagem
6. Clique em "Send"

---

### 3. Informações do Modelo

Retorna informações detalhadas sobre o modelo de Machine Learning em uso.

#### **Request**

```http
GET /modelo/info
```

#### **Parâmetros**

Nenhum parâmetro necessário.

#### **Resposta de Sucesso (200 OK)**

```json
{
  "nome": "PulmoVision ChestXRay v2",
  "arquitetura": "EfficientNetB0",
  "versao": "2.0",
  "data_criacao": "2024-01-20T14:30:00",
  "acuracia_validacao": 0.94,
  "dataset_size": 5000,
  "epocas": 30,
  "observacoes": "Modelo com transfer learning e data augmentation aprimorado",
  "carregado": true,
  "diretorio": "modelo_pulmonares_20240120_143000",
  "classes": ["normal", "pneumonia", "tuberculose"],
  "parametros_treinaveis": 4123456,
  "img_height": 224,
  "img_width": 224
}
```

#### **Campos da Resposta**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nome` | string | Nome do modelo |
| `arquitetura` | string | Arquitetura da rede neural |
| `versao` | string | Versão do modelo |
| `data_criacao` | string | Data de criação do modelo (ISO 8601) |
| `acuracia_validacao` | float | Acurácia no conjunto de validação |
| `dataset_size` | integer | Tamanho do dataset de treinamento |
| `epocas` | integer | Número de épocas de treinamento |
| `observacoes` | string | Observações sobre o modelo |
| `carregado` | boolean | Indica se o modelo está carregado |
| `diretorio` | string | Diretório do modelo |
| `classes` | array | Lista de classes detectadas |
| `parametros_treinaveis` | integer | Número de parâmetros treináveis |
| `img_height` | integer | Altura das imagens de entrada |
| `img_width` | integer | Largura das imagens de entrada |

#### **Resposta de Erro (Modelo não carregado)**

```json
{
  "erro": "Modelo não carregado",
  "carregado": false
}
```

#### **Exemplos de Uso**

**cURL:**
```bash
curl http://localhost:8000/modelo/info
```

**Python:**
```python
import requests

response = requests.get('http://localhost:8000/modelo/info')
info = response.json()

print(f"Modelo: {info['nome']}")
print(f"Arquitetura: {info['arquitetura']}")
print(f"Acurácia: {info['acuracia_validacao']:.2%}")
print(f"Dataset: {info['dataset_size']} imagens")
print(f"Classes: {', '.join(info['classes'])}")
```

---

### 4. Limitações do Sistema

Retorna as limitações conhecidas e avisos sobre o uso do sistema (transparência).

#### **Request**

```http
GET /limitacoes
```

#### **Parâmetros**

Nenhum parâmetro necessário.

#### **Resposta de Sucesso (200 OK)**

```json
{
  "limitacoes": [
    "O modelo foi treinado com um conjunto específico de dados e pode não generalizar para todas as populações",
    "Radiografias de baixa qualidade podem afetar a precisão",
    "O sistema não detecta outras doenças pulmonares além das classes treinadas",
    "Não substitui a avaliação de um radiologista profissional",
    "Recomenda-se sempre confirmação clínica e exames complementares"
  ],
  "aviso": "Este sistema é uma ferramenta de apoio à decisão clínica, não substitui avaliação médica profissional."
}
```

#### **Campos da Resposta**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `limitacoes` | array | Lista de limitações conhecidas do sistema |
| `aviso` | string | Aviso geral sobre o uso do sistema |

#### **Exemplos de Uso**

**cURL:**
```bash
curl http://localhost:8000/limitacoes
```

**Python:**
```python
import requests

response = requests.get('http://localhost:8000/limitacoes')
data = response.json()

print("Limitações do Sistema:")
for i, limitacao in enumerate(data['limitacoes'], 1):
    print(f"{i}. {limitacao}")

print(f"\nAviso: {data['aviso']}")
```

---

## Códigos de Resposta HTTP

| Código | Status | Descrição |
|--------|--------|-----------|
| `200` | OK | Requisição bem-sucedida |
| `400` | Bad Request | Erro na requisição (arquivo inválido, faltando, etc) |
| `404` | Not Found | Endpoint não encontrado |
| `500` | Internal Server Error | Erro interno do servidor |

---

## Tratamento de Erros

### Estrutura de Erro Padrão

```json
{
  "erro": "Descrição do erro"
}
```

### Erros Comuns

#### 1. Arquivo Não Enviado
```json
{
  "erro": "O arquivo de imagem é obrigatório"
}
```

#### 2. Arquivo Muito Grande
```json
{
  "erro": "Arquivo muito grande. Tamanho máximo: 10.0MB"
}
```

#### 3. Formato Inválido
```json
{
  "erro": "Tipo de arquivo não permitido. Use: jpg, jpeg, png"
}
```

#### 4. Erro de Processamento
```json
{
  "erro": "Erro interno ao processar a imagem"
}
```

### Exemplo de Tratamento de Erros (Python)

```python
import requests

url = 'http://localhost:8000/predicao'
files = {'file': open('radiografia.jpg', 'rb')}

try:
    response = requests.post(url, files=files, timeout=30)
    response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
    
    resultado = response.json()
    print(f"Sucesso: {resultado['resultado']['rotulo']}")
    
except requests.exceptions.HTTPError as e:
    if response.status_code == 400:
        erro = response.json()
        print(f"Erro na requisição: {erro['erro']}")
    elif response.status_code == 500:
        print("Erro interno do servidor")
    else:
        print(f"Erro HTTP {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("Erro: Não foi possível conectar ao servidor")
    
except requests.exceptions.Timeout:
    print("Erro: Tempo de requisição excedido")
    
except Exception as e:
    print(f"Erro inesperado: {e}")
```

---

## Exemplos de Uso

### Script Python Completo

```python
import requests
import json
from pathlib import Path

class PulmoVisionAPI:
    """Cliente Python para API PulmoVision"""
    
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
    
    def health_check(self):
        """Verifica status da API"""
        response = requests.get(f'{self.base_url}/health')
        return response.json()
    
    def predizer(self, caminho_imagem):
        """Faz predição de uma radiografia"""
        with open(caminho_imagem, 'rb') as f:
            files = {'file': f}
            response = requests.post(f'{self.base_url}/predicao', files=files)
            response.raise_for_status()
            return response.json()
    
    def info_modelo(self):
        """Obtém informações do modelo"""
        response = requests.get(f'{self.base_url}/modelo/info')
        return response.json()
    
    def limitacoes(self):
        """Obtém limitações do sistema"""
        response = requests.get(f'{self.base_url}/limitacoes')
        return response.json()

# Exemplo de uso
if __name__ == '__main__':
    api = PulmoVisionAPI()
    
    # 1. Verificar saúde da API
    print("Verificando API...")
    health = api.health_check()
    print(f"Status: {health['status']}\n")
    
    # 2. Obter informações do modelo
    print("Informações do Modelo:")
    info = api.info_modelo()
    print(f"  Nome: {info['nome']}")
    print(f"  Versão: {info['versao']}")
    print(f"  Acurácia: {info['acuracia_validacao']:.2%}\n")
    
    # 3. Fazer predição
    print("Analisando radiografia...")
    resultado = api.predizer('radiografia.jpg')
    
    print(f"\n{'='*60}")
    print(f"RESULTADO DA ANÁLISE")
    print(f"{'='*60}")
    print(f"Diagnóstico: {resultado['resultado']['rotulo'].upper()}")
    print(f"Confiança: {resultado['resultado']['confianca']:.2%}")
    print(f"\nProbabilidades:")
    for classe, prob in resultado['probabilidades'].items():
        barra = ' ' * int(prob * 50)
        print(f"  {classe:12s}: {barra} {prob:.2%}")
    print(f"\n{resultado['aviso_legal']}")
```

### Script de Teste Automatizado

```python
import requests
import json
import sys

def testar_api_completa():
    """Testa todos os endpoints da API"""
    base_url = 'http://localhost:8000'
    resultados = {'sucesso': 0, 'falha': 0}
    
    testes = [
        {
            'nome': 'Health Check',
            'metodo': 'GET',
            'endpoint': '/health',
            'esperado': 200,
            'validacao': lambda r: r.get('status') == 'ok'
        },
        {
            'nome': 'Informações do Modelo',
            'metodo': 'GET',
            'endpoint': '/modelo/info',
            'esperado': 200,
            'validacao': lambda r: 'nome' in r and 'versao' in r
        },
        {
            'nome': 'Limitações',
            'metodo': 'GET',
            'endpoint': '/limitacoes',
            'esperado': 200,
            'validacao': lambda r: 'limitacoes' in r
        }
    ]
    
    print("="*70)
    print("TESTE AUTOMATIZADO DA API PULMOVISION")
    print("="*70)
    
    for teste in testes:
        print(f"\n[{teste['nome']}]")
        print("-" * 70)
        
        try:
            url = base_url + teste['endpoint']
            response = requests.request(teste['metodo'], url, timeout=5)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == teste['esperado']:
                data = response.json()
                if teste['validacao'](data):
                    print(" PASSOU")
                    resultados['sucesso'] += 1
                else:
                    print(" FALHOU (validação)")
                    resultados['falha'] += 1
            else:
                print(f" FALHOU (esperado {teste['esperado']})")
                resultados['falha'] += 1
                
        except Exception as e:
            print(f" ERRO: {e}")
            resultados['falha'] += 1
    
    # Resumo
    print("\n" + "="*70)
    print(f"RESUMO: {resultados['sucesso']} sucessos, {resultados['falha']} falhas")
    print("="*70)
    
    return resultados['falha'] == 0

if __name__ == '__main__':
    sucesso = testar_api_completa()
    sys.exit(0 if sucesso else 1)
```

---

## Limitações e Considerações

### Limitações Técnicas

1. **Generalização do Modelo**
   - O modelo foi treinado com datasets específicos
   - Pode ter desempenho reduzido em populações não representadas no treinamento
   - Recomenda-se validação com dados locais antes do uso clínico

2. **Qualidade da Imagem**
   - Radiografias de baixa qualidade afetam a precisão
   - Imagens com artefatos podem gerar falsos positivos/negativos
   - Posicionamento adequado do paciente é importante

3. **Escopo de Detecção**
   - Detecta apenas: normal, pneumonia, tuberculose
   - Não identifica outras patologias pulmonares
   - Não diferencia subtipos ou severidade

4. **Desempenho**
   - Tempo de resposta: ~1-3 segundos por imagem
   - Depende da infraestrutura do servidor
   - Recomendado uso de GPU para produção

### Considerações Médicas

**IMPORTANTE: Este sistema é uma ferramenta de apoio à decisão clínica**

-  **Use para:** Triagem inicial, segunda opinião, apoio educacional
-  **Não use para:** Diagnóstico definitivo, decisões terapêuticas isoladas
-  **Sempre:** Confirme com avaliação médica profissional
-  **Recomenda-se:** Exames complementares e avaliação clínica completa

### Responsabilidades

- O usuário é responsável pela interpretação e uso dos resultados
- A API fornece apenas predições estatísticas baseadas em dados de treinamento
- Decisões médicas devem ser tomadas por profissionais qualificados
- Mantenha sempre o paciente como foco principal do cuidado

---

## 📞 Suporte e Contato

### Reportar Problemas

Para reportar bugs ou problemas técnicos:
- Verifique os logs em `logs/api.log`
- Execute `python manage.py check` para diagnóstico
- Abra uma issue no repositório do projeto

### Solução de Problemas Comuns

#### API não responde
```bash
# Verificar se o servidor está rodando
curl http://localhost:8000/health

# Verificar logs
tail -f logs/api.log
```

#### Erro "Modelo não carregado"
```bash
# Verificar estrutura de diretórios
ls -la modelos/saved_models/

# Cada modelo deve ter:
# - modelo.keras
# - config.json
# - info_modelo.json
```

#### Erro ao processar imagem
- Verifique se a imagem é válida (abra com visualizador)
- Confirme formato (jpg, jpeg, png)
- Verifique tamanho (máx 10MB)

---

## Licença

Este projeto está sob licença MIT.

---

## Histórico de Versões

### v1.0.0 (2025-12-16)
- Lançamento inicial
- Endpoints: health, predição, modelo/info, limitações
- Detecção de 3 classes
- Carregamento automático do modelo mais recente
- Validação de imagens
- Logging completo

---

**Desenvolvido com ❤️ para melhorar o diagnóstico de doenças pulmonares**