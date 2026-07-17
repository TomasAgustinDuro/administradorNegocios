"""Repositorio de productos.

Capa de acceso a datos para la entidad Product.
Todas las funciones reciben una sesión de SQLAlchemy y operan
directamente contra la base de datos.
"""

from sqlalchemy.orm import Session
from app.models import Product


def find_product_by_id(product_id: int, db: Session) -> Product | None:
    """Busca un producto por su ID.

    Args:
        product_id: Identificador del producto.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Product o None si no existe.
    """
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(product_data: dict, db: Session) -> Product:
    """Persiste un nuevo producto en la base de datos.

    Args:
        product_data: Diccionario con los campos del producto.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Product creada y refrescada.
    """
    new_product = Product(**product_data)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def update_product(
    product: Product, updated_data: dict, db: Session
) -> Product:
    """Actualiza campos de un producto existente.

    Args:
        product: Instancia de Product previamente obtenida.
        updated_data: Diccionario campo-valor a modificar.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Product actualizada y refrescada.
    """
    for field, value in updated_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(product: Product, db: Session) -> None:
    """Elimina un producto de la base de datos.

    Recibe la instancia del producto ya resuelta por la capa
    de servicio (no hace lookup interno por ID).

    Args:
        product: Instancia de Product a eliminar.
        db: Sesión activa de SQLAlchemy.
    """
    db.delete(product)
    db.commit()
