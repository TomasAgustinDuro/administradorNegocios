# Administrador de Negocios

Sistema de gestión para negocios. Permite registrar ventas, manejar el inventario de productos y consultar movimientos de stock.

---

## Arquitectura

```
administradorNegocios/
├── backend/
│   ├── app/
│   │   ├── main.py            # Punto de entrada FastAPI + CORS
│   │   ├── config.py          # Configuración por variables de entorno
│   │   ├── database.py        # Engine SQLAlchemy, sesión y get_db()
│   │   ├── models.py          # Modelos SQLAlchemy (tablas)
│   │   ├── routers/           # Controladores HTTP (endpoints)
│   │   ├── schemas/           # Esquemas Pydantic (validación)
│   │   ├── services/          # Lógica de negocio
│   │   └── repositories/      # Acceso a datos (queries)
│   └── tests/
│       └── unit/              # Tests unitarios (pytest)
└── frontend/
    └── src/
        ├── Products/           # Módulo de productos (listado + formulario)
        │   └── components/     # ProductForm
        ├── Ventas/             # Módulo de ventas (listado + formulario)
        │   └── components/     # VentasForm
        ├── shared/             # Componentes compartidos (Navbar)
        ├── services/           # Capa de comunicación HTTP (fetchData)
        └── Utilities/          # Validadores y helpers
```

- **Frontend**: React 18 + Vite. CSS Modules para estilos por componente.
- **Backend**: FastAPI + SQLAlchemy. API REST bajo `/api/v1/`.
- **Base de datos**: SQLite en desarrollo (`dev.db`), PostgreSQL en producción (solo cambiar `DATABASE_URL`).

---

## Tecnologías

### Frontend

| Paquete | Versión | Rol |
|---|---|---|
| `react` | ^18.3.1 | Librería de UI |
| `react-dom` | ^18.3.1 | Renderizado en el DOM |
| `react-router-dom` | ^6.26.1 | Ruteo del lado del cliente |
| `prop-types` | ^15.x | Validación de props en runtime |
| `vite` | ^5.4.0 | Bundler y servidor de desarrollo |

### Backend

| Paquete | Versión | Rol |
|---|---|---|
| `fastapi` | 0.139.0 | Framework web |
| `uvicorn` | 0.50.0 | Servidor ASGI |
| `sqlalchemy` | 2.x | ORM y acceso a base de datos |
| `pydantic` | 2.13.4 | Validación de datos |
| `pydantic-settings` | 2.14.2 | Configuración tipada |
| `python-dotenv` | 1.2.2 | Carga de `.env` |
| `pytest` | latest | Framework de testing |

---

## Modelos de datos

### Product

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer (PK) | Identificador único |
| `name` | String | Nombre del producto |
| `price` | Float | Precio de venta |
| `quantity` | Integer | Stock disponible |

### Sales

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer (PK) | Identificador único |
| `total` | Float | Monto total de la venta |
| `date` | DateTime | Fecha y hora de la venta |
| `status` | String | Estado (`active` / `cancelled`) |

### SaleItem

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer (PK) | Identificador único |
| `sale_id` | Integer (FK) | Referencia a la venta |
| `product_id` | Integer (FK) | Referencia al producto |
| `quantity` | Integer | Cantidad vendida |

### Inventory (Movimientos)

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer (PK) | Identificador único |
| `product_id` | Integer (FK) | Referencia al producto |
| `type` | String | Tipo (`entry`, `sale`, `adjustment`, `loss`) |
| `quantity` | Integer | Cantidad del movimiento |
| `reason` | String (nullable) | Motivo del movimiento |
| `date` | DateTime | Fecha y hora del registro |

---

## Endpoints de la API

### Productos (`/api/v1/products`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/products/` | Lista todos los productos |
| `POST` | `/api/v1/products/` | Crea un nuevo producto |
| `GET` | `/api/v1/products/{id}` | Detalle de un producto |
| `PUT` | `/api/v1/products/{id}` | Actualiza parcialmente un producto |
| `DELETE` | `/api/v1/products/{id}` | Elimina un producto |

### Ventas (`/api/v1/sales`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/sales/` | Lista todas las ventas |
| `POST` | `/api/v1/sales/` | Registra una nueva venta |
| `GET` | `/api/v1/sales/{id}` | Detalle de una venta |
| `POST` | `/api/v1/sales/{id}/cancel` | Cancela una venta |

### Movimientos de inventario (`/api/v1/movements`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/movements/` | Lista movimientos (filtrable por `product_id`) |
| `POST` | `/api/v1/movements/` | Registra un movimiento |

### Health Check

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/health` | Estado del servicio |

---

## Instalación local

### Requisitos previos

- Python 3.10+
- Node.js 18+
- npm 9+

### 1. Backend

```bash
cd backend
python -m venv .venv

# Windows:
.venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

El backend queda en `http://localhost:8000`.
Documentación interactiva en `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

El frontend queda en `http://localhost:5173`.

---

## Variables de entorno

### Backend (`backend/.env`)

| Variable | Default | Descripción |
|---|---|---|
| `APP_ENV` | `local` | Entorno (`local`, `production`) |
| `APP_PORT` | `8000` | Puerto del servidor |
| `DATABASE_URL` | `sqlite:///./dev.db` | URL de conexión a la DB |

### Frontend (`frontend/.env`)

| Variable | Descripción |
|---|---|
| `VITE_API_URL` | URL base del backend (ej: `http://localhost:8000/api/v1`) |

---

## Tests

```bash
cd backend
.venv\Scripts\activate
pytest -q --tb=short
```

Para correr un módulo específico:

```bash
pytest tests/unit/test_sales_service.py -q
```

Con cobertura:

```bash
pytest --cov=app --cov-report=term-missing -q
```
