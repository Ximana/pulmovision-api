# PulmoVision API

API REST para detecção de doenças pulmonares (pneumonia e tuberculose) em radiografias torácicas usando Deep Learning.

## Repositórios Relacionados

Este projeto faz parte de um ecossistema composto por três componentes principais:

### Modelo de Inteligência Artificial
- **Descrição:** Treinamento e validação do modelo de Deep Learning
- **Repositório:** https://github.com/Ximana/pulmovision-modelo

### ⚙️ Backend – PulmoVision API
- **Descrição:** API REST responsável por servir o modelo treinado
- **Repositório:** Este repositório

### Frontend – Aplicação Web
- **Descrição:** Interface web para upload de imagens e visualização dos resultados
- **Repositório:** https://github.com/Ximana/pulmovision-frontend

## Características

- Detecção de 3 classes: normal, pneumonia, tuberculose
- Baseado em EfficientNetB0
- API stateless (sem banco de dados)
- Validação rigorosa de imagens
- Disclaimer médico automático
- Logs detalhados
- Pronto para produção

## Pré-requisitos

- Python 3.9+
- Modelo treinado (.keras)

## Instalação

```bash
# Clone o repositório
git clone https://github.com/Ximana/pulmovision-api.git
cd pulmovision-api

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# Coloque seu modelo treinado em:
# modelos/saved_models/modelo_pulmonares_XXXXXXXX_XXXXXX/

# Execute
python manage.py runserver
```

## Endpoints

### 1. Health Check
```bash
GET /health
```

### 2. Predição (Principal)
```bash
POST /predicao
Content-Type: multipart/form-data

file: 
```

Resposta:
```json
{
  "resultado": {
    "rotulo": "tuberculose",
    "confianca": 0.92
  },
  "probabilidades": {
    "tuberculose": 0.92,
    "pneumonia": 0.06,
    "normal": 0.02
  },
  "modelo": {
    "nome": "PulmoVision ChestXRay",
    "arquitetura": "EfficientNetB0",
    "versao": "1.0"
  },
  "aviso_legal": "..."
}
```

### 3. Informações do Modelo
```bash
GET /modelo/info
```

### 4. Limitações
```bash
GET /limitacoes
```

## Testando

```bash
# Health check
curl http://localhost:8000/health

# Predição
curl -X POST http://localhost:8000/predicao \
  -F "file=@radiografia.jpg"
```

## Produção

```bash
# Com Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Segurança

- Validação de tipo MIME
- Limite de tamanho de arquivo
- Headers de segurança
- Rate limiting
- CORS configurável

## Licença  
Este projeto está licenciado sob a **MIT License**.  

## Contato  
📧 Email: **pauloximana@gmail.com**  
🌐 GitHub: [ximana](https://github.com/Ximana) 

## Autor

Paulo João Ximana