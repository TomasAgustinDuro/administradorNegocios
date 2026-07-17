# Administrador de Negocios

Sistema de gestión para negocios. Permite registrar ventas, manejar el inventario de productos y gestionar devoluciones.

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
│       └── unit/              # Tests unitarios (unittest)
└── src/                        # Frontend en React + Vite
    ├── Context/                # Contextos globales (React Context API)
    ├── Inventario/             # Módulo de inventario
    ├── Devoluciones/           # Módulo de devoluciones
    └── shared/                 # Componentes compartidos (Navbar)
```

- **Frontend**: React 18 + Vite. Se comunica con el backend vía HTTP.
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
# Desde la raíz del proyecto
npm install
npm run dev
```

El frontend queda en `http://localhost:5173`.

---

## Variables de entorno

Definir en `backend/.env` o como variables del sistema:

| Variable | Default | Descripción |
|---|---|---|
| `APP_ENV` | `local` | Entorno (`local`, `production`) |
| `APP_PORT` | `8000` | Puerto del servidor |
| `DATABASE_URL` | `sqlite:///./dev.db` | URL de conexión a la DB |

Para producción: `DATABASE_URL=postgresql://user:pass@host:5432/db_name`

---

## Tests

```bash
cd backend
.venv\Scripts\python.exe -m unittest discover -s tests/unit -p "test_*.py" -v
```
