"""Tests unitarios para app.services.sales.

Cubre happy path y escenarios de error para cada función del servicio.
"""

import unittest
from datetime import datetime, timezone
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from app.models import Product, Sales
from app.services.sales import (
    cancel_sale_service,
    create_sale_service,
    get_sale_by_id_service,
    list_sales_service,
)
from app.schemas.sales import SalesCreateRequest, SaleItem


class TestCreateSaleService(unittest.TestCase):
    """Tests para la creación de ventas."""

    def setUp(self) -> None:
        """Configura mocks y datos de prueba."""
        self.mock_db = Mock(spec=Session)

        # Crear datos de entrada válidos
        self.sale_data = SalesCreateRequest(items=[SaleItem(product_id=1, quantity=2)])

        # Crear mock de producto
        self.mock_product = Mock(spec=Product)
        self.mock_product.id = 1
        self.mock_product.price = 1500.0
        self.mock_product.quantity = 20

    @patch("app.services.sales.find_product_by_id")
    @patch("app.services.sales.create_sale")
    def test_creates_sale_with_correct_total(
        self, mock_create_sale, mock_find_product
    ) -> None:
        """Debe calcular el total como precio × cantidad."""
        # Configurar mocks
        mock_find_product.return_value = self.mock_product
        mock_create_sale.return_value = {
            "id": 1,
            "total": 3000.0,
            "status": "active",
            "date": datetime.now(timezone.utc),
        }

        # Ejecutar
        result = create_sale_service(self.sale_data, self.mock_db)

        # Verificar resultado
        self.assertEqual(result["total"], 3000.0)
        self.assertEqual(result["status"], "active")
        self.assertEqual(result["id"], 1)

        # Verificar que se llamó a find_product_by_id correctamente
        mock_find_product.assert_called_with(1, self.mock_db)

    @patch("app.services.sales.find_product_by_id")
    @patch("app.services.sales.create_movement")
    def test_decreases_product_stock(
        self, mock_create_movement, mock_find_product
    ) -> None:
        """Debe descontar el stock del producto vendido."""
        # Configurar mock
        mock_find_product.return_value = self.mock_product

        # Ejecutar
        with patch("app.services.sales.create_sale"):
            create_sale_service(self.sale_data, self.mock_db)

        # Verificar que el stock se decrementó
        self.assertEqual(self.mock_product.quantity, 18)

    @patch("app.services.sales.find_product_by_id")
    @patch("app.services.sales.create_movement")
    @patch("app.services.sales.create_sale")
    def test_registers_sale_movement(
        self, mock_create_sale, mock_create_movement, mock_find_product
    ) -> None:
        """Debe registrar un movimiento de tipo 'sale' en inventario."""
        # Configurar mocks
        mock_find_product.return_value = self.mock_product

        # Ejecutar
        create_sale_service(self.sale_data, self.mock_db)

        # Verificar que se creó el movimiento
        mock_create_movement.assert_called()
        call_args = mock_create_movement.call_args[0][0]
        self.assertEqual(call_args["type"], "sale")
        self.assertEqual(call_args["quantity"], 2)

    @patch("app.services.sales.find_product_by_id")
    def test_raises_if_product_not_found(self, mock_find_product) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        # Configurar mock para devolver None (producto no encontrado)
        mock_find_product.return_value = None

        # Ejecutar y verificar que lanza ValueError
        with self.assertRaises(ValueError) as context:
            create_sale_service(self.sale_data, self.mock_db)

        self.assertIn("not found", str(context.exception))

    @patch("app.services.sales.find_product_by_id")
    def test_raises_if_stock_insufficient(self, mock_find_product) -> None:
        """Debe lanzar ValueError si el stock es insuficiente."""
        # Configurar mock con stock bajo
        self.mock_product.quantity = 1  # Solo 1 pero se quieren 2
        mock_find_product.return_value = self.mock_product

        # Ejecutar y verificar que lanza ValueError
        with self.assertRaises(ValueError) as context:
            create_sale_service(self.sale_data, self.mock_db)

        self.assertIn("not in stock", str(context.exception))


class TestListSalesService(unittest.TestCase):
    """Tests para listar ventas."""

    def setUp(self) -> None:
        self.mock_db = Mock(spec=Session)

    @patch("app.services.sales.list_sales")
    def test_returns_all_sales(self, mock_list_sales) -> None:
        """Debe devolver todas las ventas."""
        mock_list_sales.return_value = [
            {"id": 1, "total": 1000, "status": "active"},
            {"id": 2, "total": 2000, "status": "cancelled"},
        ]

        result = list_sales_service(self.mock_db)

        self.assertEqual(len(result), 2)
        mock_list_sales.assert_called_with(self.mock_db)


class TestCancelSaleService(unittest.TestCase):
    """Tests para cancelar ventas."""

    def setUp(self) -> None:
        self.mock_db = Mock(spec=Session)
        self.mock_sale = Mock(spec=Sales)
        self.mock_sale.id = 1
        self.mock_sale.status = "active"
        self.mock_sale.items = [Mock(product_id=1, quantity=2)]

        self.mock_product = Mock(spec=Product)
        self.mock_product.id = 1
        self.mock_product.quantity = 18

    @patch("app.services.sales.find_product_by_id")
    @patch("app.services.sales.find_sale_by_id")
    @patch("app.services.sales.cancel_sale")
    @patch("app.services.sales.create_movement")
    def test_cancels_sale_and_restores_stock(
        self,
        mock_create_movement,
        mock_cancel_sale,
        mock_find_sale,
        mock_find_product,
    ) -> None:
        """Debe cancelar venta y restaurar stock."""
        mock_find_sale.return_value = self.mock_sale
        mock_find_product.return_value = self.mock_product
        mock_cancel_sale.return_value = {"id": 1, "status": "cancelled"}

        result = cancel_sale_service(1, self.mock_db)

        self.assertEqual(result["status"], "cancelled")
        # Verificar que el stock se restauró
        self.assertEqual(self.mock_product.quantity, 20)

    @patch("app.services.sales.find_sale_by_id")
    def test_raises_if_sale_not_found(self, mock_find_sale) -> None:
        """Debe lanzar ValueError si la venta no existe."""
        mock_find_sale.return_value = None

        with self.assertRaises(ValueError) as context:
            cancel_sale_service(999, self.mock_db)

        self.assertIn("not found", str(context.exception))

    @patch("app.services.sales.find_sale_by_id")
    def test_raises_if_sale_already_cancelled(self, mock_find_sale) -> None:
        """Debe lanzar ValueError si la venta ya está cancelada."""
        self.mock_sale.status = "cancelled"
        mock_find_sale.return_value = self.mock_sale

        with self.assertRaises(ValueError) as context:
            cancel_sale_service(1, self.mock_db)

        self.assertIn("already cancelled", str(context.exception))


class TestGetSaleByIdService(unittest.TestCase):
    """Tests para obtener venta por ID."""

    def setUp(self) -> None:
        self.mock_db = Mock(spec=Session)

    @patch("app.services.sales.find_sale_by_id")
    def test_returns_sale_by_id(self, mock_find_sale) -> None:
        """Debe devolver la venta con el ID solicitado."""
        mock_sale = {"id": 1, "total": 1000, "status": "active"}
        mock_find_sale.return_value = mock_sale

        result = get_sale_by_id_service(1, self.mock_db)

        self.assertEqual(result["id"], 1)
        mock_find_sale.assert_called_with(1, self.mock_db)

    @patch("app.services.sales.find_sale_by_id")
    def test_raises_if_sale_not_found(self, mock_find_sale) -> None:
        """Debe lanzar ValueError si la venta no existe."""
        mock_find_sale.return_value = None

        with self.assertRaises(ValueError) as context:
            get_sale_by_id_service(999, self.mock_db)

        self.assertIn("not found", str(context.exception))
