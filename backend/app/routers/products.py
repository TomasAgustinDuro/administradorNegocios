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
from app.schemas.products import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse,
)
from app.services.products import (
    create_product_service,
    modify_product_service,
    get_specific_product_service,
    delete_product_service
)
from app.models import Product
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/v1/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    """Retorna todos los productos registrados en el catálogo."""
    return db.query(Product).all()

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product_data: ProductCreateRequest, db:Session = Depends(get_db)):
    """Crea un nuevo producto en el catálogo.

    Args:
        product_data: Datos del producto (name, price, quantity).

    Raises:
        HTTPException 404: Si ocurre un error de validación de negocio.
    """
    try:
        return create_product_service(product_data, db)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

@router.put("/{product_id}", response_model=ProductResponse, status_code=200)
def modify_product(product_id: int, product_data: ProductUpdateRequest, db:Session = Depends(get_db)):
    """Actualiza parcialmente un producto existente.

    Args:
        product_id: ID del producto a actualizar.
        product_data: Campos a modificar (solo los enviados se actualizan).

    Raises:
        HTTPException 404: Si el producto no existe.
    """
    try:
        return modify_product_service(product_id, product_data, db)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    

@router.get("/{product_id}", response_model=ProductResponse, status_code=200)
def get_specific_product(product_id: int, db:Session = Depends(get_db)):
    """Obtiene un producto específico por su ID.

    Args:
        product_id: ID del producto a consultar.

    Raises:
        HTTPException 404: Si el producto no existe.
    """
    try:
        return get_specific_product_service(product_id, db)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db:Session = Depends(get_db)):
    """Elimina un producto del almacén por su ID.

    Args:
        product_id: Identificador único del producto a eliminar.

    Raises:
        HTTPException 404: Si el producto no existe en el almacén.
    """
    try:
        return delete_product_service(product_id, db)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
