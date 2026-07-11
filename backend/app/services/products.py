"""Capa de servicio para el recurso Producto.

Contiene la lógica de negocio de productos, desacoplada del transporte HTTP.
Las funciones reciben datos puros y lanzan ValueError si algo falla.
"""
from app.services.inventory import create_movement_record

def create_product_service(data, products_store: list[dict]) -> dict:
    """Crea un nuevo producto y lo almacena.

    Args:
        data: Objeto con name, price y quantity del producto.
        products_store: Lista de productos existentes.

    Returns:
        Diccionario con el producto creado (incluye id generado).
    """
    new_id = len(products_store) + 1

    new_product = {
        "id": new_id,
        "name": data.name,
        "price": data.price,
        "quantity": data.quantity,
    }

    products_store.append(new_product)
    return new_product


def modify_product_service(
    product_id: int, data, products_store: list[dict], movements_store: list[dict]
) -> dict:
    """Actualiza parcialmente un producto existente.

    Solo modifica los campos que fueron enviados (no None).
    Si el campo modificado es 'quantity', registra un movimiento
    de tipo 'Adjustment' en el inventario.

    Args:
        product_id: ID del producto a actualizar.
        data: Objeto con los campos a modificar.
        products_store: Lista de productos existentes.
        movements_store: Lista de movimientos de inventario donde se
            registra el ajuste cuando cambia la cantidad.

    Returns:
        Diccionario con el producto actualizado.

    Raises:
        ValueError: Si el producto no existe.
    """
    producto = next(
        (item for item in products_store if item["id"] == product_id), None
    )



    if not producto:
        raise ValueError(f"Product {product_id} not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        producto[field] = value

        if field == "quantity":
            create_movement_record(producto['id'], "adjustment", value, "modify product", movements_store)

    return producto


def get_specific_product_service(
    product_id: int, products_store: list[dict]
) -> dict:
    """Obtiene un producto específico por su ID.

    Args:
        product_id: ID del producto a consultar.
        products_store: Lista de productos existentes.

    Returns:
        Diccionario con los datos del producto.

    Raises:
        ValueError: Si el producto no existe.
    """
    producto = next(
        (item for item in products_store if item["id"] == product_id), None
    )

    if not producto:
        raise ValueError(f"Product {product_id} not found")

    return producto


def delete_product_service(
    product_id: int, products_store: list[dict]
) -> None:
    """Elimina un producto del almacén por su ID.

    Args:
        product_id: ID del producto a eliminar.
        products_store: Lista de productos existentes.

    Raises:
        ValueError: Si el producto no existe.
    """
    producto = next(
        (item for item in products_store if item["id"] == product_id), None
    )

    if not producto:
        raise ValueError(f"Product {product_id} not found")

    products_store.remove(producto)
