# PulmoVision API

API REST para detecção de doenças pulmonares em radiografias torácicas.

## Início Rápido

### Instalação

```bash
# Clonar repositório
git clone https://github.com/Ximana/pulmovision-api.git
cd pulmovision-api

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações
```

### Colocar Modelo

Coloque o modelo treinado em:
```
app/models/modelo_pulmonares.keras
```

### Executar

```bash
# Desenvolvimento
uvicorn app.main:app --reload

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build
docker build -t pulmovision-api .

# Run
docker run -p 8000:8000 pulmovision-api

# Ou com docker-compose
docker-compose up
```

## Documentação

Acesse a documentação interativa:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### 1. Health Check
```bash
GET /health
```

### 2. Predição (Principal)
```bash
POST /predict
Content-Type: multipart/form-data

# Exemplo com curl
curl -X POST "http://localhost:8000/predict" \\
  -H "accept: application/json" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@radiografia.jpg"
```

### 3. Informações do Modelo
```bash
GET /model
```

### 4. Limitações
```bash
GET /limitations
```

## Testes

```bash
# Executar testes
pytest

# Com coverage
pytest --cov=app tests/
```

## Exemplo de Uso

```python
import requests

# URL da API
url = "http://localhost:8000/predict"

# Enviar imagem
with open("radiografia.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

# Processar resultado
if response.status_code == 200:
    result = response.json()
    print(f"Diagnóstico: {result['resultado']['rotulo']}")
    print(f"Confiança: {result['resultado']['confianca']:.2%}")
else:
    print(f"Erro: {response.json()}")
```

## Avisos Importantes

- **NÃO usar como diagnóstico definitivo**
- Sempre supervisionar com profissional qualificado
- Ler limitações em /limitations
- Sistema em fase de pesquisa

## Licença

MIT License