"""Router de Movimientos de Inventario.

Registra y consulta movimientos de stock por producto.
Los movimientos son inmutables: una vez creados no se modifican ni eliminan.
Tipos válidos: 'entry' (ingreso), 'sale' (venta), 'adjustment' (ajuste), 'loss' (merma).

Endpoints disponibles:
  - GET    /api/v1/movements/              → Listar movimientos (filtrable por product_id via query param)
  - POST   /api/v1/movements/              → Registrar un movimiento
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.inventory import MovementCreateRequest, MovementResponse
from app.services.inventory import (
    list_movements_service,
    register_movement_service,
)
from app.models import Inventory
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/v1/movements", tags=["Inventory"])


@router.get("/", response_model=list[MovementResponse], )
def list_movements(db: Session = Depends(get_db), product_id: Optional[int] = None):
    """Lista movimientos de inventario, con filtro opcional por producto.

    Query params:
        product_id: Si se proporciona, filtra movimientos del producto indicado.
    """
    return list_movements_service(db, product_id)


@router.post("/", response_model=MovementResponse, status_code=201)
def register_movement(movement_data: MovementCreateRequest, db: Session = Depends(get_db)):
    """Registra un nuevo movimiento de inventario para un producto.

    Args:
        movement_data: Datos del movimiento (product_id, type, quantity, reason).

    Raises:
        HTTPException 404: Si el product_id no existe en el catálogo.
    """
    try:
        return register_movement_service(movement_data, db)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
