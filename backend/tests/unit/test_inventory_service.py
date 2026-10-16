"""Tests unitarios para app.services.inventory.

Cubre happy path y escenarios de error para cada función del servicio.
Se mockean las dependencias del repositorio y la sesión de SQLAlchemy.
"""

from unittest.mock import patch, MagicMock
import pytest

from app.models import Product
from app.schemas.inventory import MovementCreateRequest, MovementResponse
from app.services.inventory import (
    list_movements_service,
    register_movement_service,
)


REPO_PATH = "app.services.inventory"


class TestListMovementsService:
    """Tests para el listado de movimientos."""

    @patch(f"{REPO_PATH}.find_all_movements")
    def test_returns_all_movements_without_filter(self, mock_find: MagicMock) -> None:
        """Debe retornar todos los movimientos sin filtro."""
        mock_db = MagicMock()
        mock_find.return_value = [
            {
                "id": 1,
                "product_id": 1,
                "type": "entry",
                "quantity": 10,
                "reason": "restock",
            },
            {
                "id": 2,
                "product_id": 2,
                "type": "sale",
                "quantity": 5,
                "reason": "venta",
            },
        ]

        result = list_movements_service(mock_db)

        mock_find.assert_called_once_with(mock_db, None)
        assert len(result) == 2

    @patch(f"{REPO_PATH}.find_all_movements")
    def test_passes_product_id_filter(self, mock_find: MagicMock) -> None:
        """Debe pasar product_id al repositorio."""
        mock_db = MagicMock()
        mock_find.return_value = [
            {
                "id": 1,
                "product_id": 5,
                "type": "entry",
                "quantity": 10,
                "reason": "restock",
            }
        ]

        result = list_movements_service(mock_db, product_id=5)

        mock_find.assert_called_once_with(mock_db, 5)
        assert len(result) == 1

    @patch(f"{REPO_PATH}.find_all_movements")
    def test_returns_empty_list_when_no_movements(self, mock_find: MagicMock) -> None:
        """Debe retornar lista vacía si no hay movimientos."""
        mock_db = MagicMock()
        mock_find.return_value = []

        result = list_movements_service(mock_db)

        assert result == []


class TestRegisterMovementService:
    """Tests para el registro de movimientos."""

    def setUp(self) -> None:
        """Configura datos de prueba."""
        self.mock_db = MagicMock()
        self.mock_product = MagicMock(spec=Product)
        self.mock_product.id = 1
        self.mock_product.quantity = 20

    @patch(f"{REPO_PATH}.create_movement")
    @patch(f"{REPO_PATH}.find_product_by_id")
    def test_registers_movement_for_existing_product(
        self, mock_find_product: MagicMock, mock_create: MagicMock
    ) -> None:
        """Debe registrar movimiento si el producto existe."""
        mock_db = MagicMock()
        mock_product = MagicMock(spec=Product)
        mock_product.id = 1

        mock_find_product.return_value = mock_product
        mock_create.return_value = {
            "id": 1,
            "product_id": 1,
            "type": "entry",
            "quantity": 10,
            "reason": "restock",
        }

        request = MovementCreateRequest(
            product_id=1, type="entry", quantity=10, reason="restock"
        )
        result = register_movement_service(request, mock_db)

        mock_find_product.assert_called_once_with(1, mock_db)
        mock_create.assert_called_once()
        assert result["product_id"] == 1
        assert result["type"] == "entry"

    @patch(f"{REPO_PATH}.find_product_by_id")
    def test_raises_if_product_not_found(self, mock_find_product: MagicMock) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        mock_db = MagicMock()
        mock_find_product.return_value = None

        request = MovementCreateRequest(
            product_id=999, type="entry", quantity=10, reason="restock"
        )

        with pytest.raises(ValueError, match="not found"):
            register_movement_service(request, mock_db)

    @patch(f"{REPO_PATH}.find_product_by_id")
    @patch(f"{REPO_PATH}.create_movement")
    def test_registers_all_movement_fields(
        self, mock_create: MagicMock, mock_find_product: MagicMock
    ) -> None:
        """Debe registrar todos los campos del movimiento."""
        mock_db = MagicMock()
        mock_product = MagicMock(spec=Product)
        mock_product.id = 1

        mock_find_product.return_value = mock_product
        mock_create.return_value = {
            "id": 1,
            "product_id": 1,
            "type": "adjustment",
            "quantity": 5,
            "reason": "corrección",
        }

        request = MovementCreateRequest(
            product_id=1, type="adjustment", quantity=5, reason="corrección"
        )
        register_movement_service(request, mock_db)

        # Verificar que se creó con los datos correctos
        call_args = mock_create.call_args[0][0]
        assert call_args["product_id"] == 1
        assert call_args["type"] == "adjustment"
        assert call_args["quantity"] == 5
        assert call_args["reason"] == "corrección"
