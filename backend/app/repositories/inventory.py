"""Repositorio de movimientos de inventario.

Capa de acceso a datos para la entidad Inventory.
Todas las funciones reciben una sesión de SQLAlchemy y operan
directamente contra la base de datos.
"""

from sqlalchemy.orm import Session
from typing import Optional
from app.models import Inventory


def create_movement(movement_data: dict, db: Session) -> Inventory:
    """Persiste un nuevo movimiento de inventario en la base de datos.

    Args:
        movement_data: Diccionario con los campos del movimiento.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Inventory creada y refrescada.
    """
    new_movement = Inventory(**movement_data)

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)
    return new_movement

def find_all_movements(db: Session, product_id:Optional[int] = None):
    query = db.query(Inventory)

    if product_id:
       query = query.filter(Inventory.product_id == product_id)
    
    return query.all()