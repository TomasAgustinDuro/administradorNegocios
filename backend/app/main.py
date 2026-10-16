from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import Base, engine
from app.exceptions import BusinessLogicError, ErrorResponse
from app.routers.inventory import router as inventory_router
from app.routers.products import router as products_router
from app.routers.sales import router as sales_router

app = FastAPI(
    title="AdminNegocios",
    description="API genérica para administración de negocios",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(products_router)
app.include_router(sales_router)
app.include_router(inventory_router)


@app.get("/api/v1/health", tags=["Health"])
def health_check():
    """Verifica que el servicio esté activo y responde con el entorno actual."""
    return {"status": "healthy", "environment": settings.app_env}


@app.exception_handler(BusinessLogicError)
async def business_logic_exception_handler(
    request: Request, exc: BusinessLogicError
) -> JSONResponse:
    """Maneja errores de lógica de negocio.

    Devuelve 400/422 con contrato de error estructurado.
    """
    error_response = ErrorResponse(
        error=exc.message,
        code=exc.code,
        timestamp=datetime.utcnow(),
        details=exc.details,
    )
    return JSONResponse(
        status_code=exc.http_status,
        content=error_response.model_dump(mode="json"),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Maneja excepciones inesperadas.

    Devuelve 500 SIN exponer detalles internos (solo code + timestamp).
    En logs se registra el error completo para debugging.
    """
    import logging

    logger = logging.getLogger(__name__)
    logger.exception(f"Unhandled exception: {exc}")

    error_response = ErrorResponse(
        error="Internal server error",
        code="INTERNAL_SERVER_ERROR",
        timestamp=datetime.utcnow(),
        details=None,  # No exponer internals en producción
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(mode="json"),
    )
