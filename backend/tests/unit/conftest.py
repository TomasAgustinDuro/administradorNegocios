"""Fixtures compartidas para los tests unitarios de servicios.

Provee stores frescos y objetos Pydantic reutilizables para cada test.
Importar desde los archivos de test para reutilizar.
"""

from app.schemas.products import ProductCreateRequest, ProductUpdateRequest
from app.schemas.sales import SalesCreateRequest, SaleItem
from app.schemas.inventory import MovementCreateRequest


def get_products_store() -> list[dict]:
    """Store de productos con un producto inicial para tests."""
    return [
        {"id": 1, "name": "Coca Cola", "price": 1500.0, "quantity": 20},
    ]


def get_empty_products_store() -> list[dict]:
    """Store de productos vacío."""
    return []


def get_sales_store() -> list[dict]:
    """Store de ventas vacío."""
    return []


def get_movements_store() -> list[dict]:
    """Store de movimientos de inventario vacío."""
    return []


def get_product_create_request() -> ProductCreateRequest:
    """Request válido para crear un producto."""
    return ProductCreateRequest(name="Pepsi", price=1200.0, quantity=15)


def get_product_update_name_request() -> ProductUpdateRequest:
    """Request para actualizar solo el nombre de un producto."""
    return ProductUpdateRequest(name="Coca Cola Zero")


def get_product_update_quantity_request() -> ProductUpdateRequest:
    """Request para actualizar solo la cantidad de un producto."""
    return ProductUpdateRequest(quantity=50)


def get_sale_create_request() -> SalesCreateRequest:
    """Request válido para crear una venta de 2 unidades del producto 1."""
    return SalesCreateRequest(
        items=[SaleItem(product_id=1, quantity=2)]
    )


def get_sale_exceeds_stock_request() -> SalesCreateRequest:
    """Request de venta que excede el stock disponible."""
    return SalesCreateRequest(
        items=[SaleItem(product_id=1, quantity=999)]
    )


def get_sale_invalid_product_request() -> SalesCreateRequest:
    """Request de venta con un product_id inexistente."""
    return SalesCreateRequest(
        items=[SaleItem(product_id=999, quantity=1)]
    )


def get_movement_create_request() -> MovementCreateRequest:
    """Request válido para registrar un movimiento de inventario."""
    return MovementCreateRequest(
        product_id=1, type="entry", quantity=10, reason="restock"
    )


def get_movement_invalid_product_request() -> MovementCreateRequest:
    """Request de movimiento con product_id inexistente."""
    return MovementCreateRequest(
        product_id=999, type="entry", quantity=5, reason="restock"
    )
