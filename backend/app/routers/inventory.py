"""Router de Movimientos de Inventario.

Registra y consulta movimientos de stock por producto.
Los movimientos son inmutables: una vez creados no se modifican ni eliminan.
Tipos válidos: 'entry' (ingreso), 'sale' (venta), 'adjustment' (ajuste), 'loss' (merma).

Endpoints disponibles:
  - GET    /api/v1/movements/              → Listar movimientos (filtrable por product_id via query param)
  - POST   /api/v1/movements/              → Registrar un movimiento
"""

from typing import Optional

from fastapi import APIRouter, HTTPException
from app.schemas.inventory import MovementCreateRequest, MovementResponse
from app.routers.products import products_store
from datetime import datetime

router = APIRouter(prefix="/api/v1/movements", tags=["Inventory"])

movements_store: list[dict] = []


@router.get("/", response_model=list[MovementResponse])
def list_movements(product_id: Optional[int] = None):
    """Lista todos los movimientos de inventario, con filtro opcional por producto.

    Query params:
        product_id: Si se proporciona, filtra movimientos del producto indicado.

    Returns:
        Lista de movimientos registrados.
    """
    if product_id:
        return [m for m in movements_store if m["product_id"] == product_id]
    return movements_store


@router.post("/", response_model=MovementResponse, status_code=201)
def register_movement(movement_data: MovementCreateRequest):
    """Registra un nuevo movimiento de inventario para un producto.

    Valida que el producto exista antes de registrar el movimiento.
    Genera automáticamente: id y fecha del movimiento.

    Args:
        movement_data: Datos del movimiento (product_id, type, quantity, reason).

    Raises:
        HTTPException 404: Si el product_id no existe en el catálogo.
    """
    product = next((item for item in products_store if item["id"] == movement_data.product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_id = len(movements_store) + 1

    new_movement = {
        "id": new_id,
        "product_id": movement_data.product_id,
        "type": movement_data.type,
        "quantity": movement_data.quantity,
        "reason": movement_data.reason,
        "date": datetime.now()
    }

    movements_store.append(new_movement)
    return new_movement
