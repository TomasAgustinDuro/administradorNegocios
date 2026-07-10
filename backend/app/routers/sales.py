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

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.schemas.sales import SaleResponse, SalesCreateRequest
from app.routers.products import products_store

router = APIRouter(prefix="/api/v1/sales", tags=["Sales"])

sales_store: list[dict] = []


@router.get("/", response_model=list[SaleResponse])
def list_sales():
    """Retorna todas las ventas registradas (activas y canceladas)."""
    return sales_store


@router.post("/", response_model=SaleResponse, status_code=201)
def create_sale(sale_data: SalesCreateRequest):
    """Registra una nueva venta calculando el total a partir de los ítems.

    Valida que cada product_id exista en el catálogo de productos.
    Genera automáticamente: id, total, fecha y status='active'.

    Args:
        sale_data: Lista de ítems vendidos (product_id + quantity).

    Raises:
        HTTPException 404: Si algún product_id no existe en el catálogo.
    """
    new_id = len(sales_store) + 1
    total = 0

    for item in sale_data.items:
        product = next((p for p in products_store if p["id"] == item.product_id), None)

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        total += product["price"] * item.quantity

    new_sale = {
        "id": new_id,
        "items": sale_data.items,
        "total": total,
        "date": datetime.now(),
        "status": "active"
    }

    sales_store.append(new_sale)
    return new_sale


@router.post("/{sale_id}/cancel", response_model=SaleResponse, status_code=200)
def cancel_sale(sale_id: int):
    """Cancela una venta existente cambiando su status a 'cancelled'.

    No elimina el registro, preservando la trazabilidad.

    Args:
        sale_id: ID de la venta a cancelar.

    Raises:
        HTTPException 404: Si la venta no existe.
        HTTPException 400: Si la venta ya fue cancelada previamente.
    """
    sale = next((i for i in sales_store if i["id"] == sale_id), None)

    if not sale:
        raise HTTPException(status_code=404, detail=f"Sale with id {sale_id} not found")
    if sale["status"] == "cancelled":
        raise HTTPException(status_code=400, detail="Sale already cancelled")

    sale["status"] = "cancelled"
    return sale


@router.get("/{sale_id}", response_model=SaleResponse, status_code=200)
def get_sale_by_id(sale_id: int):
    """Obtiene una venta específica por su ID.

    Args:
        sale_id: ID de la venta a consultar.

    Raises:
        HTTPException 404: Si la venta no existe.
    """
    sale = next((i for i in sales_store if i["id"] == sale_id), None)

    if not sale:
        raise HTTPException(status_code=404, detail=f"Sale with id {sale_id} not found")

    return sale
