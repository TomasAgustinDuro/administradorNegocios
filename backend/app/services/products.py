"""Capa de servicio para el recurso Producto.

Contiene la lógica de negocio de productos, desacoplada del transporte HTTP.
Las funciones reciben datos puros y lanzan ValueError si algo falla.
"""

from datetime import UTC, datetime

from app.repositories.inventory import create_movement
from app.repositories.products import (
    create_product,
    delete_product,
    find_product_by_id,
    update_product,
)
from sqlalchemy.orm import Session
from app.models import Product  # ORM
from app.schemas.products import ProductResponse


def create_product_service(data, db: Session) -> ProductResponse:
    """Crea un nuevo producto y lo persiste en la base de datos.

    Args:
        data: Objeto con name, price y quantity del producto.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Product creada.
    """

    product: Product = create_product(data.model_dump(), db)

    return ProductResponse(
        id=product.id, name=product.name, price=product.price, quantity=product.quantity
    )


def modify_product_service(product_id: int, data, db: Session) -> ProductResponse:
    """Actualiza parcialmente un producto existente.

    Solo modifica los campos que fueron enviados (no None).
    Si el campo modificado es 'quantity', registra un movimiento
    de tipo 'Adjustment' en el inventario.

    Args:
        product_id: ID del producto a actualizar.
        data: Objeto Pydantic con los campos a modificar.
        db: Sesión activa de SQLAlchemy.

    Returns:
        ProductResponse con los datos actualizados.

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
                "date": datetime.now(UTC),
            },
            db,
        )

    updated_product = update_product(producto, update_data, db)

    return ProductResponse(
        id=updated_product.id,
        name=updated_product.name,
        price=updated_product.price,
        quantity=updated_product.quantity,
    )


def get_specific_product_service(product_id: int, db: Session) -> ProductResponse:
    """Obtiene un producto específico por su ID.

    Args:
        product_id: ID del producto a consultar.
        db: Sesión activa de SQLAlchemy.

    Returns:
        ProductResponse con los datos del producto.

    Raises:
        ValueError: Si el producto no existe.
    """
    producto = find_product_by_id(product_id, db)

    if not producto:
        raise ValueError(f"Product {product_id} not found")

    return ProductResponse(
        id=producto.id,
        name=producto.name,
        price=producto.price,
        quantity=producto.quantity,
    )


def delete_product_service(product_id: int, db: Session) -> None:
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
