"""Capa de servicio para Movimientos de Inventario.

Contiene la lógica de negocio de movimientos de stock, desacoplada
del transporte HTTP. Las funciones reciben una sesión de SQLAlchemy
y delegan la persistencia al repositorio.
"""

from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.products import find_product_by_id
from app.repositories.inventory import (
    find_all_movements,
    create_movement,
)


def list_movements_service(
    db: Session, product_id: Optional[int] = None
) -> list:
    """Lista movimientos de inventario, con filtro opcional.

    Args:
        db: Sesión activa de SQLAlchemy.
        product_id: Si se proporciona, filtra por ese producto.

    Returns:
        Lista de instancias Inventory.
    """
    return find_all_movements(db, product_id)


def register_movement_service(
    movement_data, db: Session
) -> dict:
    """Registra un nuevo movimiento de inventario.

    Valida que existan movimientos previos del producto (como proxy
    de existencia) antes de persistir el nuevo registro.

    Args:
        movement_data: Objeto Pydantic con product_id, type,
            quantity y reason.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia Inventory creada.

    Raises:
        ValueError: Si el product_id no tiene registros previos.
    """
    product = find_product_by_id(movement_data.product_id, db)

    if not product:
        raise ValueError(
            f"Product {movement_data.product_id} not found"
        )

    movement_dict = {
        "product_id": movement_data.product_id,
        "type": movement_data.type,
        "quantity": movement_data.quantity,
        "reason": movement_data.reason,
    }

    return create_movement(movement_dict, db)
