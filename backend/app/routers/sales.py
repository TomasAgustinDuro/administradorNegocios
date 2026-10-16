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

from app.auth import verify_token
from app.database import get_db
from app.exceptions import BusinessLogicError
from app.schemas.sales import SaleResponse, SalesCreateRequest
from app.services.sales import (
    cancel_sale_service,
    create_sale_service,
    get_sale_by_id_service,
    list_sales_service,
)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/sales", tags=["Sales"])


@router.get("/", response_model=list[SaleResponse])
def list_sales(db: Session = Depends(get_db)):
    """Retorna todas las ventas registradas (activas y canceladas)."""
    return list_sales_service(db)


@router.post("/", response_model=SaleResponse, status_code=201)
def create_sale(
    sale_data: SalesCreateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(verify_token),
):
    """Registra una nueva venta calculando el total a partir de los ítems.

    Args:
        sale_data: Lista de ítems vendidos (product_id + quantity).

    Raises:
        BusinessLogicError 400: Si algún product_id no existe en el catálogo.
    """
    try:
        return create_sale_service(sale_data, db)
    except ValueError as error:
        raise BusinessLogicError(
            message=str(error),
            code="SALE_CREATION_FAILED",
            http_status=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/{sale_id}/cancel", response_model=SaleResponse, status_code=200)
def cancel_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_token),
):
    """Cancela una venta existente cambiando su status a 'cancelled'.

    Args:
        sale_id: ID de la venta a cancelar.

    Raises:
        BusinessLogicError 400: Si la venta no existe o ya fue cancelada.
    """
    try:
        return cancel_sale_service(sale_id, db)
    except ValueError as error:
        raise BusinessLogicError(
            message=str(error),
            code="SALE_CANCELLATION_FAILED",
            http_status=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/{sale_id}", response_model=SaleResponse, status_code=200)
def get_sale_by_id(sale_id: int, db: Session = Depends(get_db)):
    """Obtiene una venta específica por su ID.

    Args:
        sale_id: ID de la venta a consultar.

    Raises:
        BusinessLogicError 404: Si la venta no existe.
    """
    try:
        return get_sale_by_id_service(sale_id, db)
    except ValueError as error:
        raise BusinessLogicError(
            message=str(error),
            code="SALE_NOT_FOUND",
            http_status=status.HTTP_404_NOT_FOUND,
        )
