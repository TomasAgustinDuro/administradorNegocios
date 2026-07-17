"""Router de Ventas.

Expone los endpoints para el recurso Venta.
Las ventas son inmutables: no se modifican ni eliminan.
Solo pueden ser canceladas mediante el endpoint /cancel.

Endpoints disponibles:
  - GET    /api/v1/sales/              → Listar todas las ventas
  - POST   /api/v1/sales/              → Registrar una nueva venta
  - GET    /api/v1/sales/{id}          → Obtener una venta por ID
  - POST   /api/v1/sales/{id}/cancel   → Cancelar una venta
"""

from fastapi import APIRouter, HTTPException,Depends
from app.schemas.sales import SaleResponse, SalesCreateRequest
from app.services.sales import (
    create_sale_service,
    list_sales_service,
    cancel_sale_service,
    get_sale_by_id_service,
)
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/v1/sales", tags=["Sales"])


@router.get("/", response_model=list[SaleResponse])
def list_sales(db: Session = Depends(get_db)):
    """Retorna todas las ventas registradas (activas y canceladas)."""
    return list_sales_service(db)


@router.post("/", response_model=SaleResponse, status_code=201)
def create_sale(sale_data: SalesCreateRequest, db: Session = Depends(get_db)):
    """Registra una nueva venta calculando el total a partir de los ítems.

    Args:
        sale_data: Lista de ítems vendidos (product_id + quantity).

    Raises:
        HTTPException 404: Si algún product_id no existe en el catálogo.
    """
    try:
        return create_sale_service(sale_data, db)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/{sale_id}/cancel", response_model=SaleResponse, status_code=200)
def cancel_sale(sale_id: int, db: Session = Depends(get_db)):
    """Cancela una venta existente cambiando su status a 'cancelled'.

    Args:
        sale_id: ID de la venta a cancelar.

    Raises:
        HTTPException 404: Si la venta no existe.
        HTTPException 400: Si la venta ya fue cancelada previamente.
    """
    try:
        return cancel_sale_service(sale_id, db)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{sale_id}", response_model=SaleResponse, status_code=200)
def get_sale_by_id(sale_id: int, db: Session = Depends(get_db)):
    """Obtiene una venta específica por su ID.

    Args:
        sale_id: ID de la venta a consultar.

    Raises:
        HTTPException 404: Si la venta no existe.
    """
    try:
        return get_sale_by_id_service(sale_id, db)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
