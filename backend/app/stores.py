"""Almacenes en memoria compartidos entre routers y services.

Centraliza los stores para evitar imports circulares entre módulos.
En producción estos se reemplazarán por una base de datos real.
"""

products_store: list[dict] = [
    {"id": 1, "name": "Coca Cola", "price": 1500.0, "quantity": 20},
]

sales_store: list[dict] = []

movements_store: list[dict] = []
