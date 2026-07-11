from fastapi import FastAPI
from app.config import settings
from app.routers.products import router as products_router
from app.routers.sales import router as sales_router
from app.routers.inventory import router as inventory_router

app = FastAPI(
    title="AdminNegocios",
    description="API genérica para administración de negocios",
    version="0.1.0"
)

app.include_router(products_router)
app.include_router(sales_router)
app.include_router(inventory_router)

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    """Verifica que el servicio esté activo y responde con el entorno actual."""
    return {
        "status": "healthy",
        "environment": settings.app_env
    }