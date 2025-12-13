FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \\
    libgomp1 \\
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app/ ./app/

# Criar diretório para modelos
RUN mkdir -p /app/app/models

# Expor porta
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \\
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]