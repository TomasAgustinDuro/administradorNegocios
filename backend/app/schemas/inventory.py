"""Esquemas Pydantic para el recurso Movimiento de Inventario.

Define los contratos de entrada y salida para los endpoints de movimientos
de inventario (ingresos, egresos, ajustes).
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class MovementCreateRequest(BaseModel):
    """Esquema de validación para registrar un movimiento de inventario.

    Attributes:
        product_id: ID del producto afectado. Debe existir en el catálogo.
        type: Tipo de movimiento ('in', 'out', 'adjustment').
        quantity: Cantidad del movimiento. Debe ser mayor a cero.
        reason: Motivo opcional del movimiento (ej: 'compra', 'rotura').
    """

    product_id: int
    type: Literal["entry", "sale", "adjustment", "loss"]
    quantity: int = Field(gt=0)
    reason: str | None = None


class MovementResponse(BaseModel):
    """Esquema de respuesta que representa un movimiento registrado.

    Attributes:
        id: Identificador único del movimiento (generado por el backend).
        product_id: ID del producto afectado.
        type: Tipo de movimiento realizado.
        quantity: Cantidad del movimiento.
        reason: Motivo del movimiento, si fue proporcionado.
        date: Fecha y hora en que se registró el movimiento.
    """

    id: int
    product_id: int
    type: str
    quantity: int
    reason: str | None = None
    date: datetime
