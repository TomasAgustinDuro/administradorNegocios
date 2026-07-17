"""Tests unitarios para app.services.inventory.

Cubre happy path y escenarios de error para cada función del servicio.
Se mockean las dependencias del repositorio y la sesión de SQLAlchemy.
"""

from unittest.mock import patch, MagicMock
import pytest

from app.services.inventory import (
    list_movements_service,
    register_movement_service,
)
from tests.unit.conftest import (
    get_movement_create_request,
    get_movement_invalid_product_request,
)


REPO_PATH = "app.services.inventory"


class TestListMovementsService:
    """Tests para el listado de movimientos."""

    @patch(f"{REPO_PATH}.find_all_movements")
    def test_returns_all_movements_without_filter(
        self, mock_find: MagicMock
    ) -> None:
        """Debe retornar todos los movimientos sin filtro."""
        mock_db = MagicMock()
        mock_find.return_value = [{"id": 1}, {"id": 2}]

        result = list_movements_service(mock_db)

        mock_find.assert_called_once_with(mock_db, None)
        assert len(result) == 2

    @patch(f"{REPO_PATH}.find_all_movements")
    def test_passes_product_id_filter(
        self, mock_find: MagicMock
    ) -> None:
        """Debe pasar product_id al repositorio."""
        mock_db = MagicMock()
        mock_find.return_value = [{"id": 1, "product_id": 5}]

        result = list_movements_service(mock_db, product_id=5)

        mock_find.assert_called_once_with(mock_db, 5)
        assert len(result) == 1

    @patch(f"{REPO_PATH}.find_all_movements")
    def test_returns_empty_list_when_no_movements(
        self, mock_find: MagicMock
    ) -> None:
        """Debe retornar lista vacía si no hay movimientos."""
        mock_db = MagicMock()
        mock_find.return_value = []

        result = list_movements_service(mock_db)

        assert result == []


class TestRegisterMovementService:
    """Tests para el registro de movimientos."""

    @patch(f"{REPO_PATH}.create_movement")
    @patch(f"{REPO_PATH}.find_all_movements")
    def test_registers_movement_for_existing_product(
        self,
        mock_find: MagicMock,
        mock_create: MagicMock,
    ) -> None:
        """Debe registrar movimiento si el producto tiene registros."""
        mock_db = MagicMock()
        mock_find.return_value = [{"id": 1, "product_id": 1}]
        mock_create.return_value = {
            "id": 2,
            "product_id": 1,
            "type": "entry",
            "quantity": 10,
            "reason": "restock",
        }

        request = get_movement_create_request()
        result = register_movement_service(request, mock_db)

        mock_find.assert_called_once_with(mock_db, 1)
        mock_create.assert_called_once_with(
            {
                "product_id": 1,
                "type": "entry",
                "quantity": 10,
                "reason": "restock",
            },
            mock_db,
        )
        assert result["product_id"] == 1
        assert result["type"] == "entry"

    @patch(f"{REPO_PATH}.find_all_movements")
    def test_raises_if_product_not_found(
        self, mock_find: MagicMock
    ) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        mock_db = MagicMock()
        mock_find.return_value = []

        request = get_movement_invalid_product_request()

        with pytest.raises(ValueError, match="Product 999 not found"):
            register_movement_service(request, mock_db)
