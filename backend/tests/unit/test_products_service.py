"""Tests unitarios para app.services.products.

Cubre happy path y escenarios de error para cada función del servicio.
"""

import unittest
from app.services.products import (
    create_product_service,
    modify_product_service,
    get_specific_product_service,
    delete_product_service,
)
from tests.unit.conftest import (
    get_products_store,
    get_empty_products_store,
    get_movements_store,
    get_product_create_request,
    get_product_update_name_request,
    get_product_update_quantity_request,
)


class TestCreateProductService(unittest.TestCase):
    """Tests para la creación de productos."""

    def setUp(self) -> None:
        self.products_store = get_empty_products_store()
        self.request = get_product_create_request()

    def test_creates_product_with_correct_fields(self) -> None:
        """Debe crear un producto con id, name, price y quantity."""
        result = create_product_service(self.request, self.products_store)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Pepsi")
        self.assertEqual(result["price"], 1200.0)
        self.assertEqual(result["quantity"], 15)

    def test_appends_product_to_store(self) -> None:
        """Debe agregar el producto al store."""
        create_product_service(self.request, self.products_store)

        self.assertEqual(len(self.products_store), 1)

    def test_increments_id_sequentially(self) -> None:
        """Debe asignar id incremental basado en el largo del store."""
        store = get_products_store()
        result = create_product_service(self.request, store)

        self.assertEqual(result["id"], 2)


class TestModifyProductService(unittest.TestCase):
    """Tests para la modificación parcial de productos."""

    def setUp(self) -> None:
        self.products_store = get_products_store()
        self.movements_store = get_movements_store()

    def test_updates_name_only(self) -> None:
        """Debe actualizar solo el nombre sin tocar otros campos."""
        request = get_product_update_name_request()
        result = modify_product_service(
            1, request, self.products_store, self.movements_store
        )

        self.assertEqual(result["name"], "Coca Cola Zero")
        self.assertEqual(result["price"], 1500.0)
        self.assertEqual(result["quantity"], 20)

    def test_updates_quantity_and_registers_movement(self) -> None:
        """Debe actualizar quantity y registrar un movimiento de ajuste."""
        request = get_product_update_quantity_request()
        modify_product_service(
            1, request, self.products_store, self.movements_store
        )

        self.assertEqual(self.products_store[0]["quantity"], 50)
        self.assertEqual(len(self.movements_store), 1)
        self.assertEqual(self.movements_store[0]["type"], "adjustment")

    def test_raises_if_product_not_found(self) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        request = get_product_update_name_request()

        with self.assertRaises(ValueError) as context:
            modify_product_service(
                999, request, self.products_store, self.movements_store
            )

        self.assertIn("Product 999 not found", str(context.exception))


class TestGetSpecificProductService(unittest.TestCase):
    """Tests para la consulta de un producto por ID."""

    def setUp(self) -> None:
        self.products_store = get_products_store()

    def test_returns_product_by_id(self) -> None:
        """Debe retornar el producto correcto."""
        result = get_specific_product_service(1, self.products_store)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Coca Cola")

    def test_raises_if_product_not_found(self) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        with self.assertRaises(ValueError) as context:
            get_specific_product_service(999, self.products_store)

        self.assertIn("Product 999 not found", str(context.exception))


class TestDeleteProductService(unittest.TestCase):
    """Tests para la eliminación de productos."""

    def setUp(self) -> None:
        self.products_store = get_products_store()

    def test_removes_product_from_store(self) -> None:
        """Debe eliminar el producto del store."""
        delete_product_service(1, self.products_store)

        self.assertEqual(len(self.products_store), 0)

    def test_raises_if_product_not_found(self) -> None:
        """Debe lanzar ValueError si el producto no existe."""
        with self.assertRaises(ValueError) as context:
            delete_product_service(999, self.products_store)

        self.assertIn("Product 999 not found", str(context.exception))


if __name__ == "__main__":
    unittest.main()
