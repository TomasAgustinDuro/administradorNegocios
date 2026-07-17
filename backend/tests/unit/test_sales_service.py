"""Tests unitarios para app.services.sales.

Cubre happy path y escenarios de error para cada función del servicio.
"""

import unittest
from app.services.sales import (
    create_sale_service,
    list_sales_service,
    cancel_sale_service,
    get_sale_by_id_service,
)
from tests.unit.conftest import (
    get_products_store,
    get_sales_store,
    get_movements_store,
    get_sale_create_request,
    get_sale_exceeds_stock_request,
    get_sale_invalid_product_request,
)


class TestCreateSaleService(unittest.TestCase):
    """Tests para la creación de ventas."""

    def setUp(self) -> None:
        self.products_store = get_products_store()
        self.sales_store = get_sales_store()
        self.movements_store = get_movements_store()
        self.request = get_sale_create_request()

    def test_creates_sale_with_correct_total(self) -> None:
        """Debe calcular el total como precio × cantidad."""
        result = create_sale_service(
            self.request, self.sales_store,
            self.products_store, self.movements_store,
        )

        # 1500.0 * 2 = 3000.0
        self.assertEqual(result["total"], 3000.0)
        self.assertEqual(result["status"], "active")
        self.assertEqual(result["id"], 1)

    def test_decreases_product_stock(self) -> None:
        """Debe descontar el stock del producto vendido."""
        create_sale_service(
            self.request, self.sales_store,
            self.products_store, self.movements_store,
        )

        self.assertEqual(self.products_store[0]["quantity"], 18)

    def test_registers_sale_movement(self) -> None:
        """Debe registrar un movimiento de tipo 'sale' en inventario."""
        create_sale_service(
            self.request, self.sales_store,
            self.products_store, self.movements_store,
        )

        self.assertEqual(len(self.movements_store), 1)
        self.assertEqual(self.movements_store[0]["type"], "sale")

    def test_raises_if_product_not_found(self) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        request = get_sale_invalid_product_request()

        with self.assertRaises(ValueError) as context:
            create_sale_service(
                request, self.sales_store,
                self.products_store, self.movements_store,
            )

        self.assertIn("Product 999 not found", str(context.exception))

    def test_raises_if_stock_insufficient(self) -> None:
        """Debe lanzar ValueError si el stock es insuficiente."""
        request = get_sale_exceeds_stock_request()

        with self.assertRaises(ValueError) as context:
            create_sale_service(
                request, self.sales_store,
                self.products_store, self.movements_store,
            )

        self.assertIn("not in stock", str(context.exception))


class TestListSalesService(unittest.TestCase):
    """Tests para el listado de ventas."""

    def test_returns_empty_list_initially(self) -> None:
        """Debe retornar lista vacía si no hay ventas."""
        sales_store = get_sales_store()
        result = list_sales_service(sales_store)

        self.assertEqual(result, [])

    def test_returns_all_sales(self) -> None:
        """Debe retornar todas las ventas creadas."""
        products_store = get_products_store()
        sales_store = get_sales_store()
        movements_store = get_movements_store()
        request = get_sale_create_request()

        create_sale_service(
            request, sales_store, products_store, movements_store
        )

        result = list_sales_service(sales_store)

        self.assertEqual(len(result), 1)


class TestCancelSaleService(unittest.TestCase):
    """Tests para la cancelación de ventas."""

    def setUp(self) -> None:
        self.products_store = get_products_store()
        self.sales_store = get_sales_store()
        self.movements_store = get_movements_store()
        self.request = get_sale_create_request()
        # Crear una venta para luego cancelarla
        create_sale_service(
            self.request, self.sales_store,
            self.products_store, self.movements_store,
        )

    def test_cancels_sale_and_restores_stock(self) -> None:
        """Debe cambiar status a 'cancelled' y restaurar stock."""
        result = cancel_sale_service(
            1, self.sales_store, self.products_store, self.movements_store
        )

        self.assertEqual(result["status"], "cancelled")
        # Stock: 20 - 2 (venta) + 2 (cancelación) = 20
        self.assertEqual(self.products_store[0]["quantity"], 20)

    def test_registers_adjustment_movement_on_cancel(self) -> None:
        """Debe registrar un movimiento de ajuste al cancelar."""
        cancel_sale_service(
            1, self.sales_store, self.products_store, self.movements_store
        )

        adjustment_movements = [
            m for m in self.movements_store if m["type"] == "adjustment"
        ]
        self.assertEqual(len(adjustment_movements), 1)

    def test_raises_if_sale_not_found(self) -> None:
        """Debe lanzar ValueError si la venta no existe."""
        with self.assertRaises(ValueError) as context:
            cancel_sale_service(
                99, self.sales_store,
                self.products_store, self.movements_store,
            )

        self.assertIn("Sale with id 99 not found", str(context.exception))

    def test_raises_if_sale_already_cancelled(self) -> None:
        """Debe lanzar ValueError si la venta ya fue cancelada."""
        cancel_sale_service(
            1, self.sales_store, self.products_store, self.movements_store
        )

        with self.assertRaises(ValueError) as context:
            cancel_sale_service(
                1, self.sales_store,
                self.products_store, self.movements_store,
            )

        self.assertIn("already cancelled", str(context.exception))


class TestGetSaleByIdService(unittest.TestCase):
    """Tests para la consulta de una venta por ID."""

    def setUp(self) -> None:
        self.products_store = get_products_store()
        self.sales_store = get_sales_store()
        self.movements_store = get_movements_store()
        request = get_sale_create_request()
        create_sale_service(
            request, self.sales_store,
            self.products_store, self.movements_store,
        )

    def test_returns_sale_by_id(self) -> None:
        """Debe retornar la venta correcta."""
        result = get_sale_by_id_service(1, self.sales_store)

        self.assertEqual(result["id"], 1)

    def test_raises_if_sale_not_found(self) -> None:
        """Debe lanzar ValueError si la venta no existe."""
        with self.assertRaises(ValueError) as context:
            get_sale_by_id_service(99, self.sales_store)

        self.assertIn("Sale with id 99 not found", str(context.exception))


if __name__ == "__main__":
    unittest.main()
