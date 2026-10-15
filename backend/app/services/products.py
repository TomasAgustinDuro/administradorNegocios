"""Capa de servicio para el recurso Producto.

Contiene la lógica de negocio de productos, desacoplada del transporte HTTP.
Las funciones reciben datos puros y lanzan ValueError si algo falla.
"""
from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.products import (
    find_product_by_id,
    create_product,
    update_product,
    delete_product,
)
from app.repositories.inventory import create_movement

def create_product_service(data, db: Session) -> dict:
    """Crea un nuevo producto y lo persiste en la base de datos.

    Args:
        data: Objeto con name, price y quantity del producto.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Product creada.
    """
    return create_product(data.model_dump(), db)


def modify_product_service(
    product_id: int, data, db: Session
) -> dict:
    """Actualiza parcialmente un producto existente.

    Solo modifica los campos que fueron enviados (no None).
    Si el campo modificado es 'quantity', registra un movimiento
    de tipo 'Adjustment' en el inventario.

    Args:
        product_id: ID del producto a actualizar.
        data: Objeto Pydantic con los campos a modificar.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Product actualizada.

    Raises:
        ValueError: Si el producto no existe.
    """
    producto = find_product_by_id(product_id, db)

    if not producto:
        raise ValueError(f"Product {product_id} not found")

    update_data = data.model_dump(exclude_unset=True)

    if "quantity" in update_data:
        create_movement(
            {
                "product_id": producto.id,
                "type": "adjustment",
                "quantity": update_data["quantity"],
                "reason": "update product",
                "date": datetime.now(),
            },
            db,
        )

    return update_product(producto, update_data, db)


def get_specific_product_service(
    product_id: int, db: Session
) -> dict:
    """Obtiene un producto específico por su ID.

    Args:
        product_id: ID del producto a consultar.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Product encontrada.

    Raises:
        ValueError: Si el producto no existe.
    """
    producto = find_product_by_id(product_id, db)

    if not producto:
        raise ValueError(f"Product {product_id} not found")

    return producto


def delete_product_service(
    product_id: int, db: Session
) -> None:
    """Elimina un producto de la base de datos por su ID.

    Args:
        product_id: ID del producto a eliminar.
        db: Sesión activa de SQLAlchemy.

    Raises:
        ValueError: Si el producto no existe.
    """
    producto = find_product_by_id(product_id, db)
    
    if not producto:
        raise ValueError(f"Product {product_id} not found")

    return delete_product(producto, db)
