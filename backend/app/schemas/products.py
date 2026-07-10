"""Esquemas Pydantic para el recurso Producto.

Define los contratos de entrada y salida para los endpoints de productos.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ProductCreateRequest(BaseModel):
    """Esquema de validación para la creación de un producto."""

    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)


class ProductUpdateRequest(BaseModel):
    """Esquema de validación para la actualización parcial de un producto."""

    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class ProductResponse(BaseModel):
    """Esquema de respuesta que representa un producto almacenado."""

    name: str
    price: float 
    quantity: int
    id: int
