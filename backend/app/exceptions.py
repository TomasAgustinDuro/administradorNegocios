"""Manejo centralizado de excepciones y errores.

Define excepciones custom y esquemas de respuesta de error
para mantener un contrato consistente en toda la API.
"""

from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Esquema unificado de respuesta de error.

    Attributes:
        error: Mensaje descriptivo del error (seguro, sin internals).
        code: Código de error interno (ej: PRODUCT_NOT_FOUND).
        timestamp: Cuándo ocurrió el error (ISO 8601).
        details: Información adicional si aplica (opcional).
    """

    error: str
    code: str
    timestamp: datetime
    details: str | None = None


class BusinessLogicError(Exception):
    """Excepción para errores de lógica de negocio.

    Se usa cuando la request es válida pero viola reglas de negocio
    (ej: producto no existe, stock insuficiente).

    Attributes:
        message: Descripción del error.
        code: Código de error interno.
        http_status: Status HTTP a devolver (default 400).
        details: Información adicional (opcional).
    """

    def __init__(
        self,
        message: str,
        code: str,
        http_status: int = status.HTTP_400_BAD_REQUEST,
        details: str | None = None,
    ):
        self.message = message
        self.code = code
        self.http_status = http_status
        self.details = details
        super().__init__(self.message)


def create_error_response(
    message: str,
    code: str,
    details: Optional[str] = None,
) -> ErrorResponse:
    """Factory para crear respuestas de error consistentes.

    Args:
        message: Mensaje descriptivo (user-facing).
        code: Código interno de error (máquina-friendly).
        details: Información adicional (opcional).

    Returns:
        ErrorResponse formateada con timestamp actual.
    """
    return ErrorResponse(
        error=message,
        code=code,
        timestamp=datetime.utcnow(),
        details=details,
    )
