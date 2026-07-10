"""Esquemas Pydantic para el recurso Venta.

Define los contratos de entrada y salida para los endpoints de ventas.
El modelo de ventas es inmutable: una vez creada, no se modifica.
Solo se puede cancelar (cambio de status), preservando trazabilidad.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SaleItem(BaseModel):
    """Representa un ítem individual dentro de una venta.

    Attributes:
        product_id: ID del producto vendido. Debe existir en el catálogo.
        quantity: Cantidad vendida. Debe ser mayor a cero.
    """

    product_id: int
    quantity: int = Field(gt=0)


class SalesCreateRequest(BaseModel):
    """Esquema de validación para registrar una nueva venta.

    El usuario solo envía la lista de ítems vendidos.
    El backend calcula total, fecha, ID y status automáticamente.

    Attributes:
        items: Lista de productos vendidos con sus cantidades. Mínimo 1 ítem.
    """

    items: list[SaleItem] = Field(min_length=1)


class SaleResponse(BaseModel):
    """Esquema de respuesta que representa una venta registrada.

    Attributes:
        id: Identificador único de la venta (generado por el backend).
        items: Lista de ítems que componen la venta.
        total: Monto total calculado (suma de precio × cantidad por ítem).
        date: Fecha y hora en que se registró la venta.
        status: Estado de la venta ('active' o 'cancelled').
    """

    id: int
    items: list[SaleItem]
    total: float
    date: datetime
    status: str


