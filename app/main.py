"""
PulmoVision API - Aplicação Principal
Sistema de detecção de doenças pulmonares via API REST
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.config import settings
from app.api.routes import health, predict, model, limitations
from app.utils.exceptions import PulmoVisionException
from app.utils.logging import setup_logging

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware de logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log todas as requisições com tempo de resposta."""
    start_time = time.time()
    
    # Log da requisição
    logger.info(f"Requisição: {request.method} {request.url.path}")
    
    # Processar requisição
    response = await call_next(request)
    
    # Calcular tempo de processamento
    process_time = time.time() - start_time
    
    # Log da resposta
    logger.info(
        f"Resposta: {request.method} {request.url.path} "
        f"[{response.status_code}] - {process_time:.3f}s"
    )
    
    # Adicionar header com tempo de processamento
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Handler global de exceções
@app.exception_handler(PulmoVisionException)
async def pulmovision_exception_handler(request: Request, exc: PulmoVisionException):
    """Trata exceções customizadas da aplicação."""
    logger.error(f"Erro PulmoVision: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": exc.error_type,
                "message": exc.detail,
                "timestamp": time.time()
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Trata exceções não previstas."""
    logger.error(f"Erro inesperado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_error",
                "message": "Erro interno do servidor. Por favor, tente novamente mais tarde.",
                "timestamp": time.time()
            }
        }
    )


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Executado na inicialização da API."""
    logger.info("=" * 60)
    logger.info("Iniciando PulmoVision API")
    logger.info(f"Versão: {settings.API_VERSION}")
    logger.info(f"Ambiente: {settings.ENVIRONMENT}")
    logger.info(f"Modelo: {settings.MODEL_NAME} v{settings.MODEL_VERSION}")
    logger.info("=" * 60)
    
    # Pré-carregar o modelo (warm-up)
    try:
        from app.core.model_loader import get_model
        model = get_model()
        logger.info("✓ Modelo carregado com sucesso")
    except Exception as e:
        logger.error(f"✗ Erro ao carregar modelo: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Executado no encerramento da API."""
    logger.info("Encerrando PulmoVision API")


# Incluir routers
app.include_router(health.router, tags=["Health"])
app.include_router(predict.router, tags=["Predição"])
app.include_router(model.router, tags=["Modelo"])
app.include_router(limitations.router, tags=["Informações"])


# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """Redireciona para a documentação."""
    return {
        "message": "PulmoVision API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_DEBUG
    )