"""Tests unitarios para app.services.products.

Cubre happy path y escenarios de error para cada función del servicio.
"""

import unittest
from datetime import datetime, timezone
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from app.models import Product
from app.schemas.products import ProductCreateRequest, ProductUpdateRequest
from app.services.products import (
    create_product_service,
    delete_product_service,
    get_specific_product_service,
    modify_product_service,
)


class TestCreateProductService(unittest.TestCase):
    """Tests para la creación de productos."""

    def setUp(self) -> None:
        self.mock_db = Mock(spec=Session)
        self.product_data = ProductCreateRequest(
            name="Pepsi", price=1200.0, quantity=15
        )

    @patch("app.services.products.create_product")
    def test_creates_product_with_correct_fields(self, mock_create_product) -> None:
        """Debe crear un producto con id, name, price y quantity."""
        mock_create_product.return_value = {
            "id": 1,
            "name": "Pepsi",
            "price": 1200.0,
            "quantity": 15,
        }

        result = create_product_service(self.product_data, self.mock_db)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Pepsi")
        self.assertEqual(result["price"], 1200.0)
        self.assertEqual(result["quantity"], 15)

    @patch("app.services.products.create_product")
    def test_appends_product_to_store(self, mock_create_product) -> None:
        """Debe llamar a create_product con datos correctos."""
        mock_create_product.return_value = {
            "id": 1,
            "name": "Pepsi",
            "price": 1200.0,
            "quantity": 15,
        }

        create_product_service(self.product_data, self.mock_db)

        # Verificar que se llamó a create_product
        mock_create_product.assert_called_once()


class TestModifyProductService(unittest.TestCase):
    """Tests para la modificación parcial de productos."""

    def setUp(self) -> None:
        self.mock_db = Mock(spec=Session)
        self.mock_product = Mock(spec=Product)
        self.mock_product.id = 1
        self.mock_product.name = "Coca Cola"
        self.mock_product.price = 1500.0
        self.mock_product.quantity = 20

    @patch("app.services.products.find_product_by_id")
    @patch("app.services.products.update_product")
    def test_updates_name_only(self, mock_update_product, mock_find_product) -> None:
        """Debe actualizar solo el nombre sin tocar otros campos."""
        request = ProductUpdateRequest(name="Coca Cola Zero")
        mock_find_product.return_value = self.mock_product
        mock_update_product.return_value = {
            "id": 1,
            "name": "Coca Cola Zero",
            "price": 1500.0,
            "quantity": 20,
        }

        result = modify_product_service(1, request, self.mock_db)

        self.assertEqual(result["name"], "Coca Cola Zero")
        self.assertEqual(result["price"], 1500.0)
        self.assertEqual(result["quantity"], 20)

    @patch("app.services.products.find_product_by_id")
    @patch("app.services.products.update_product")
    @patch("app.services.products.create_movement")
    def test_updates_quantity_and_registers_movement(
        self, mock_create_movement, mock_update_product, mock_find_product
    ) -> None:
        """Debe actualizar quantity y registrar un movimiento de ajuste."""
        request = ProductUpdateRequest(quantity=50)
        mock_find_product.return_value = self.mock_product
        mock_update_product.return_value = {
            "id": 1,
            "name": "Coca Cola",
            "price": 1500.0,
            "quantity": 50,
        }

        modify_product_service(1, request, self.mock_db)

        # Verificar que se creó el movimiento
        mock_create_movement.assert_called()
        call_args = mock_create_movement.call_args[0][0]
        self.assertEqual(call_args["type"], "adjustment")

    @patch("app.services.products.find_product_by_id")
    def test_raises_if_product_not_found(self, mock_find_product) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        request = ProductUpdateRequest(name="New Name")
        mock_find_product.return_value = None

        with self.assertRaises(ValueError) as context:
            modify_product_service(999, request, self.mock_db)

        self.assertIn("not found", str(context.exception))


class TestGetSpecificProductService(unittest.TestCase):
    """Tests para la consulta de un producto por ID."""

    def setUp(self) -> None:
        self.mock_db = Mock(spec=Session)
        self.mock_product = {
            "id": 1,
            "name": "Coca Cola",
            "price": 1500.0,
            "quantity": 20,
        }

    @patch("app.services.products.find_product_by_id")
    def test_returns_product_by_id(self, mock_find_product) -> None:
        """Debe devolver el producto con el ID solicitado."""
        mock_find_product.return_value = self.mock_product

        result = get_specific_product_service(1, self.mock_db)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Coca Cola")
        mock_find_product.assert_called_with(1, self.mock_db)

    @patch("app.services.products.find_product_by_id")
    def test_raises_if_product_not_found(self, mock_find_product) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        mock_find_product.return_value = None

        with self.assertRaises(ValueError) as context:
            get_specific_product_service(999, self.mock_db)

        self.assertIn("not found", str(context.exception))


class TestDeleteProductService(unittest.TestCase):
    """Tests para la eliminación de productos."""

    def setUp(self) -> None:
        self.mock_db = Mock(spec=Session)
        self.mock_product = Mock(spec=Product)
        self.mock_product.id = 1

    @patch("app.services.products.find_product_by_id")
    @patch("app.services.products.delete_product")
    def test_removes_product_from_store(
        self, mock_delete_product, mock_find_product
    ) -> None:
        """Debe eliminar el producto correctamente."""
        mock_find_product.return_value = self.mock_product
        mock_delete_product.return_value = None

        delete_product_service(1, self.mock_db)

        # Verificar que se llamó a delete_product
        mock_delete_product.assert_called_once_with(self.mock_product, self.mock_db)

    @patch("app.services.products.find_product_by_id")
    def test_raises_if_product_not_found(self, mock_find_product) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        mock_find_product.return_value = None

        with self.assertRaises(ValueError) as context:
            delete_product_service(999, self.mock_db)

        self.assertIn("not found", str(context.exception))
