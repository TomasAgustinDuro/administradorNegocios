"""Router de Productos.

Expone los endpoints CRUD para el recurso Producto.
Endpoints disponibles:
  - GET    /api/v1/products/          → Listar todos los productos
  - POST   /api/v1/products/          → Crear un producto
  - GET    /api/v1/products/{id}      → Obtener un producto por ID
  - PUT    /api/v1/products/{id}      → Actualizar parcialmente un producto
  - DELETE /api/v1/products/{id}      → Eliminar un producto
"""

from fastapi import APIRouter, HTTPException
from app.schemas.products import ProductCreateRequest, ProductUpdateRequest, ProductResponse

router = APIRouter(prefix="/api/v1/products", tags=["Products"])

products_store: list[dict] = [
    {"id": 1, "name": "Coca Cola", "price": 1500.0, "quantity": 20},
]

@router.get("/", response_model=list[ProductResponse])
def list_products():
    return products_store

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product_data: ProductCreateRequest):
    new_id = len(products_store) + 1

    new_product = {
        "id": new_id,
        "name": product_data.name,
        "price": product_data.price, 
        "quantity": product_data.quantity
    }

    products_store.append(new_product)
    return new_product

@router.put("/{product_id}", response_model=ProductResponse, status_code=200)
def modify_product(product_id:int, product_data: ProductUpdateRequest):

    producto = next((item for item in products_store if item["id"] == product_id), None)

    if not producto:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        producto[field] = value

    return producto

@router.get("/{product_id}", response_model=ProductResponse, status_code=200)
def get_specific_product(product_id: int):
    producto = next((item for item in products_store if item["id"] == product_id), None)

    if not producto:
        raise HTTPException(status_code=404, detail="Product not found")

    return producto

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    """Elimina un producto del almacén por su ID.

    Args:
        product_id: Identificador único del producto a eliminar.

    Raises:
        HTTPException 404: Si el producto no existe en el almacén.
    """
    producto = next((item for item in products_store if item["id"] == product_id), None)

    if not producto:
        raise HTTPException(status_code=404, detail="Product not found")

    products_store.remove(producto)
