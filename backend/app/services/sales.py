"""Capa de servicio para el recurso Venta.

Contiene la lógica de negocio de ventas, desacoplada del transporte HTTP.
Las funciones reciben datos puros y lanzan ValueError si algo falla.
El router se encarga de traducir esos errores a respuestas HTTP.
"""

from datetime import UTC, datetime

from app.repositories.inventory import create_movement
from app.repositories.products import find_product_by_id
from app.repositories.sales import cancel_sale, create_sale, find_sale_by_id, list_sales
from app.schemas.sales import SaleResponse
from sqlalchemy.orm import Session


def create_sale_service(
    sale_data,
    db: Session,
) -> SaleResponse:
    """Crea una nueva venta calculando el total a partir del catálogo.

    Registra un movimiento de tipo 'sale' en el inventario por cada ítem
    vendido, además de descontar el stock del producto.

    Args:
        sale_data: Objeto con la lista de ítems (product_id + quantity).
        sales_store: Lista de ventas existentes (store en memoria).
        products_store: Lista de productos del catálogo.
        movements_store: Lista de movimientos de inventario donde se
            registra cada descuento de stock por venta.

    Returns:
        Diccionario con la venta creada (id, items, total, date, status).

    Raises:
        ValueError: Si algún product_id no existe en el catálogo.
        ValueError: Si el stock del producto es insuficiente.
    """
    total = 0

    for item in sale_data.items:
        product = find_product_by_id(item.product_id, db)

        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        if not product.quantity >= item.quantity:
            raise ValueError(f"Product {item.product_id} not in stock")

        total += product.price * item.quantity

        product.quantity -= item.quantity

        create_movement(
            {
                "product_id": item.product_id,
                "type": "sale",
                "quantity": item.quantity,
                "reason": "sale",
                "date": datetime.now(UTC),
            },
            db,
        )

    new_sale = {"total": total, "date": datetime.now(), "status": "active"}

    items_data = [
        {"product_id": i.product_id, "quantity": i.quantity} for i in sale_data.items
    ]

    return create_sale(new_sale, items_data, db)


def list_sales_service(db: Session) -> list[SaleResponse]:
    """Retorna todas las ventas registradas.

    Args:
        sales_store: Lista de ventas almacenadas.

    Returns:
        Lista completa de ventas (activas y canceladas).
    """
    sales = list_sales(db)
    return [
        SaleResponse(
            id=sale.id,
            total=sale.total,
            date=sale.date,
            status=sale.status,
            items=[],  # Los items se incluyen si SaleResponse los mapea
        )
        for sale in sales
    ]


def cancel_sale_service(sale_id: int, db: Session) -> SaleResponse:
    """Cancela una venta existente cambiando su status a 'cancelled'.

    Restaura el stock de cada producto incluido en la venta y registra
    un movimiento de ajuste en el inventario.

    Args:
        sale_id: ID de la venta a cancelar.
        sales_store: Lista de ventas almacenadas.
        products_store: Lista de productos del catálogo (se restaura stock).
        movements_store: Lista de movimientos de inventario donde se
            registra el ajuste por cancelación.

    Returns:
        SaleResponse con la venta cancelada.

    Raises:
        ValueError: Si la venta no existe.
        ValueError: Si la venta ya fue cancelada previamente.
        ValueError: Si algún producto de la venta ya no existe.
    """
    sale = find_sale_by_id(sale_id, db)

    if not sale:
        raise ValueError(f"Sale with id {sale_id} not found")
    if sale.status == "cancelled":
        raise ValueError(f"Sale with id {sale_id} already cancelled")

    for item in sale.items:
        product = find_product_by_id(item.product_id, db)

        if not product:
            raise ValueError(f"Product {item.product_id} not found")

        product.quantity += item.quantity

        create_movement(
            {
                "product_id": item.product_id,
                "type": "sale",
                "quantity": item.quantity,
                "reason": "sale",
                "date": datetime.now(),
            },
            db,
        )

    cancelled_sale = cancel_sale(db, sale)

    return SaleResponse(
        id=cancelled_sale.id,
        total=cancelled_sale.total,
        date=cancelled_sale.date,
        status=cancelled_sale.status,
        items=[],
    )


def get_sale_by_id_service(sale_id: int, db: Session) -> SaleResponse:
    """Obtiene una venta específica por su ID.

    Args:
        sale_id: ID de la venta a consultar.
        sales_store: Lista de ventas almacenadas.

    Returns:
        SaleResponse con los datos de la venta.

    Raises:
        ValueError: Si la venta no existe.
    """
    sale = find_sale_by_id(sale_id, db)

    if not sale:
        raise ValueError(f"Sale with id {sale_id} not found")

    return SaleResponse(
        id=sale.id,
        total=sale.total,
        date=sale.date,
        status=sale.status,
        items=[],
    )
