"""Repositorio de ventas.

Capa de acceso a datos para la entidad Sales.
Todas las funciones reciben una sesión de SQLAlchemy y operan
directamente contra la base de datos.
"""

from sqlalchemy.orm import Session
from app.models import Sales, SaleItem


def create_sale(sale_data: dict, items_data: list[dict], db: Session) -> Sales:
    """Persiste una nueva venta con sus ítems en la base de datos.

    Args:
        sale_data: Diccionario con los campos de la venta.
        items_data: Lista de diccionarios con los campos de cada ítem.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Sales creada y refrescada.
    """
    new_sale = Sales(**sale_data)

    for item in items_data:
        new_sale.items.append(SaleItem(**item))

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale

def list_sales(db: Session) -> list[Sales]:
    """Retorna todas las ventas registradas.

    Args:
        db: Sesión activa de SQLAlchemy.

    Returns:
        Lista de instancias de Sales.
    """
    return db.query(Sales).all()


def cancel_sale(
    db: Session, sale: Sales
) -> Sales:
    """Cancela una venta cambiando su status a 'cancelled'.

    Args:
        db: Sesión activa de SQLAlchemy.
        sale: Instancia de Sales previamente obtenida.

    Returns:
        Instancia de Sales con status actualizado y refrescada.
    """
    sale.status = "cancelled"
    db.commit()
    db.refresh(sale)
    return sale


def find_sale_by_id(sale_id: int, db: Session) -> Sales | None:
    """Busca una venta por su ID.

    Args:
        sale_id: Identificador de la venta.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Instancia de Sales o None si no existe.
    """
    return db.query(Sales).filter(Sales.id == sale_id).first()
