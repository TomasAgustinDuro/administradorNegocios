"""Capa de servicio para el recurso Venta.

Contiene la lógica de negocio de ventas, desacoplada del transporte HTTP.
Las funciones reciben datos puros y lanzan ValueError si algo falla.
El router se encarga de traducir esos errores a respuestas HTTP.
"""

from datetime import datetime
from app.services.inventory import create_movement_record


def create_sale_service(
    sale_data, sales_store: list[dict], products_store: list[dict], movements_store: list[dict]
) -> dict:
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
    new_id = len(sales_store) + 1
    total = 0

    for item in sale_data.items:
        product = next(
            (p for p in products_store if p["id"] == item.product_id), None
        )

        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        if not product["quantity"] >= item.quantity:
            raise ValueError(f"Product {item.product_id} not in stock")

        total += product["price"] * item.quantity

        product['quantity'] -= item.quantity

        create_movement_record(
            item.product_id, "sale", item.quantity, "sale", movements_store
        )


    new_sale = {
        "id": new_id,
        "items": sale_data.items,
        "total": total,
        "date": datetime.now(),
        "status": "active",
    }

    sales_store.append(new_sale)
    return new_sale


def list_sales_service(sales_store: list[dict]) -> list[dict]:
    """Retorna todas las ventas registradas.

    Args:
        sales_store: Lista de ventas almacenadas.

    Returns:
        Lista completa de ventas (activas y canceladas).
    """
    return sales_store


def cancel_sale_service(
    sale_id: int,
    sales_store: list[dict],
    products_store: list[dict],
    movements_store: list[dict],
) -> dict:
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
        Diccionario con la venta cancelada.

    Raises:
        ValueError: Si la venta no existe.
        ValueError: Si la venta ya fue cancelada previamente.
        ValueError: Si algún producto de la venta ya no existe.
    """
    sale = next((i for i in sales_store if i["id"] == sale_id), None)

    if not sale:
        raise ValueError(f"Sale with id {sale_id} not found")
    if sale["status"] == "cancelled":
        raise ValueError(f"Sale with id {sale_id} already cancelled")

    for item in sale["items"]:
        product = next(
            (p for p in products_store if p["id"] == item.product_id), None
        )

        if not product:
            raise ValueError(f"Product {item.product_id} not found")

        product['quantity'] += item.quantity

        create_movement_record(
            item.product_id, "adjustment", item.quantity, "sale cancelled", movements_store
        )
    

    sale["status"] = "cancelled"
    return sale


def get_sale_by_id_service(sale_id: int, sales_store: list[dict]) -> dict:
    """Obtiene una venta específica por su ID.

    Args:
        sale_id: ID de la venta a consultar.
        sales_store: Lista de ventas almacenadas.

    Returns:
        Diccionario con los datos de la venta.

    Raises:
        ValueError: Si la venta no existe.
    """
    sale = next((i for i in sales_store if i["id"] == sale_id), None)

    if not sale:
        raise ValueError(f"Sale with id {sale_id} not found")

    return sale
