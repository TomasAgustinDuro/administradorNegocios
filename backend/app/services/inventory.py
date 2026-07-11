"""Capa de servicio para Movimientos de Inventario.

Contiene la lógica de negocio de movimientos de stock, desacoplada del transporte HTTP.
Las funciones reciben datos puros y lanzan ValueError si algo falla.
"""

from datetime import datetime
from typing import Optional


def create_movement_record(
    product_id: int,
    movement_type: str,
    quantity: int,
    reason: Optional[str],
    movements_store: list[dict],
) -> dict:
    """Crea un registro de movimiento de inventario (uso interno entre services).

    No valida existencia del producto — se asume que el servicio llamador
    ya lo verificó.

    Args:
        product_id: ID del producto afectado.
        movement_type: Tipo de movimiento ('entry', 'sale', 'adjustment', 'loss').
        quantity: Cantidad del movimiento.
        reason: Motivo opcional del movimiento.
        movements_store: Lista de movimientos existentes.

    Returns:
        Diccionario con el movimiento creado.
    """
    new_id = len(movements_store) + 1

    new_movement = {
        "id": new_id,
        "product_id": product_id,
        "type": movement_type,
        "quantity": quantity,
        "reason": reason,
        "date": datetime.now(),
    }

    movements_store.append(new_movement)
    return new_movement


def list_movements_service(
    movements_store: list[dict], product_id: Optional[int] = None
) -> list[dict]:
    """Lista movimientos de inventario, con filtro opcional por producto.

    Args:
        movements_store: Lista de movimientos almacenados.
        product_id: Si se proporciona, filtra solo los de ese producto.

    Returns:
        Lista de movimientos (todos o filtrados).
    """
    if product_id:
        return [m for m in movements_store if m["product_id"] == product_id]
    return movements_store


def register_movement_service(
    movement_data, movements_store: list[dict], products_store: list[dict]
) -> dict:
    """Registra un nuevo movimiento de inventario para un producto.

    Valida que el producto exista antes de registrar.
    Delega la creación del registro a create_movement_record.

    Args:
        movement_data: Objeto Pydantic con product_id, type, quantity y reason.
        movements_store: Lista de movimientos existentes.
        products_store: Lista de productos del catálogo.

    Returns:
        Diccionario con el movimiento creado.

    Raises:
        ValueError: Si el product_id no existe en el catálogo.
    """
    product = next(
        (item for item in products_store if item["id"] == movement_data.product_id),
        None,
    )

    if not product:
        raise ValueError(f"Product {movement_data.product_id} not found")

    return create_movement_record(
        movement_data.product_id,
        movement_data.type,
        movement_data.quantity,
        movement_data.reason,
        movements_store,
    )
