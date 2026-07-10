# Administrador de Negocios — Venta de Diarios

Sistema de gestión para negocios de venta de diarios y revistas. Permite registrar ventas diarias, manejar el inventario de productos y gestionar devoluciones con imagen.

---

## Descripción general

La aplicación está pensada para que un kiosco o negocio de venta de diarios pueda:

- Registrar qué diarios/revistas se vendieron en el día y a qué precio.
- Controlar el inventario de productos con código de barras (stock, vendido, restante).
- Registrar devoluciones de mercadería adjuntando una foto como evidencia.

---

## Arquitectura

El proyecto está dividido en dos capas independientes:

```
administradorNegocios/
├── backend/
│   ├── app/                    # API REST en FastAPI (nuevo)
│   │   ├── main.py            # Punto de entrada de la aplicación FastAPI
│   │   ├── config.py          # Configuración por variables de entorno
│   │   ├── routers/           # Controladores HTTP (endpoints)
│   │   ├── schemas/           # Esquemas Pydantic (validación de datos)
│   │   ├── services/          # Lógica de negocio
│   │   └── repositories/     # Acceso a datos
│   └── ventaDiariosBack/       # API REST en Django (legacy)
│       ├── diarios/            # App principal: modelos, vistas y URLs
│       ├── media/              # Archivos subidos (imágenes de devoluciones)
│       └── ventaDiariosBack/   # Configuración del proyecto Django
└── src/                        # Frontend en React + Vite
    ├── Context/                # Contextos globales (React Context API)
    ├── Devoluciones/           # Módulo de devoluciones
    └── ...                     # Resto de módulos del frontend
```

- **Frontend**: React 18 + Vite. Se comunica con el backend vía HTTP (fetch/axios).
- **Backend (FastAPI)**: API REST nueva basada en FastAPI. Expone endpoints bajo `/api/v1/`.
- **Backend (Django — legacy)**: Django 5.1 + Django REST Framework. API REST original con JSON.
- **Base de datos**: SQLite (archivo `db.sqlite3`, local) para el backend Django.
- **Archivos multimedia**: Django sirve las imágenes de devoluciones desde `/media/`.

---

## Tecnologías y dependencias

### Frontend (`package.json`)

| Paquete | Versión | Rol |
|---|---|---|
| `react` | ^18.3.1 | Librería de UI |
| `react-dom` | ^18.3.1 | Renderizado en el DOM |
| `react-router-dom` | ^6.26.1 | Ruteo del lado del cliente |
| `vite` | ^5.4.0 | Bundler y servidor de desarrollo |
| `@vitejs/plugin-react-swc` | ^3.5.0 | Compilación rápida de React con SWC |
| `eslint` | ^9.8.0 | Linter de código |

### Backend — FastAPI (`backend/requirements.txt`)

| Paquete | Versión | Rol |
|---|---|---|
| `fastapi` | 0.139.0 | Framework web principal |
| `uvicorn` | 0.50.0 | Servidor ASGI |
| `pydantic` | 2.13.4 | Validación de datos y esquemas |
| `pydantic-settings` | 2.14.2 | Configuración tipada por variables de entorno |
| `python-dotenv` | 1.2.2 | Carga de `.env` |

### Backend — Django (legacy)

| Paquete | Rol |
|---|---|
| `Django 5.1` | Framework web principal |
| `djangorestframework` | Construcción de la API REST |
| `django-cors-headers` | Habilita CORS para que el frontend pueda consumir la API |
| `Pillow` | Procesamiento de imágenes (requerido por `ImageField`) |
| `SQLite` | Base de datos embebida (sin instalación adicional) |

---

## Modelos de datos

### `DiarioVendido`
Representa un diario o revista vendido en el día.

| Campo | Tipo | Descripción |
|---|---|---|
| `nombre` | CharField(255) | Nombre del diario/revista |
| `valor` | IntegerField | Precio de venta (no puede ser negativo) |

### `Inventario`
Controla el stock de un producto identificado por código de barras.

| Campo | Tipo | Descripción |
|---|---|---|
| `nombre` | CharField(255) | Nombre del producto |
| `codigo_barras` | CharField(255, unique) | Código de barras único |
| `stock` | IntegerField | Cantidad total recibida |
| `vendido` | IntegerField | Cantidad vendida acumulada |
| `restante` | IntegerField | Stock restante (`stock - vendido`) |

### `Devolucion`
Registra una devolución con su imagen de evidencia.

| Campo | Tipo | Descripción |
|---|---|---|
| `imagen` | ImageField | Foto de la devolución (guardada en `/media/devoluciones/`) |
| `fecha` | DateField | Fecha de la devolución |

---

## Endpoints de la API

---

### Backend FastAPI (`http://localhost:8000`)

#### Productos (`/api/v1/products`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/products/` | Lista todos los productos |
| `POST` | `/api/v1/products/` | Crea un nuevo producto |
| `GET` | `/api/v1/products/<id>` | Detalle de un producto |
| `PUT` | `/api/v1/products/<id>` | Actualiza parcialmente un producto |
| `DELETE` | `/api/v1/products/<id>` | Elimina un producto |

**Body POST:**
```json
{
  "name": "Revista Gente",
  "price": 1500.0,
  "quantity": 50
}
```

**Body PUT** (todos los campos son opcionales):
```json
{
  "name": "Nuevo nombre",
  "price": 1800.0,
  "quantity": 45
}
```

#### Health Check

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/health` | Estado del servicio |

---

### Backend Django — legacy (`http://localhost:8000`)

### Diarios vendidos

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/diarios/api/diarios/` | Lista todos los diarios vendidos |
| `POST` | `/diarios/api/diarios/` | Registra un nuevo diario vendido |
| `GET` | `/diarios/api/diarios/<id>/` | Detalle de un diario |
| `PUT` | `/diarios/api/diarios/<id>/` | Actualiza un diario |
| `DELETE` | `/diarios/api/diarios/<id>/` | Elimina un diario |
| `DELETE` | `/diarios/api/diarios/eliminar_todos/` | Elimina todos los registros de ventas |

**Body POST/PUT:**
```json
{
  "nombre": "La Nación",
  "valor": 1500
}
```

### Inventario

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/diarios/api/inventarios/` | Lista todos los productos del inventario |
| `POST` | `/diarios/api/inventarios/` | Crea un nuevo producto |
| `GET` | `/diarios/api/inventarios/<id>/` | Detalle de un producto |
| `PUT` | `/diarios/api/inventarios/<id>/` | Actualiza stock o ventas de un producto |
| `DELETE` | `/diarios/api/inventarios/<id>/` | Elimina un producto |

**Body POST:**
```json
{
  "nombre": "Revista Gente",
  "codigo_barras": "7891234560001",
  "stock": 50,
  "vendido": 0
}
```

**Body PUT** (todos los campos son opcionales):
```json
{
  "stock": 60,
  "vendido": 5
}
```
> Nota: el campo `vendido` en PUT es **incremental** — suma al valor existente.

### Devoluciones

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/diarios/api/devoluciones/` | Lista todas las devoluciones |
| `POST` | `/diarios/api/devoluciones/` | Registra una nueva devolución |
| `GET` | `/diarios/api/devoluciones/<id>/` | Detalle de una devolución |
| `PUT` | `/diarios/api/devoluciones/<id>/` | Actualiza la fecha de una devolución |
| `DELETE` | `/diarios/api/devoluciones/<id>/` | Elimina una devolución |

**Body POST** (`multipart/form-data`):
```
imagen: <archivo de imagen>
fecha: 2024-08-15
```

---

## Instalación local

### Requisitos previos

- Python 3.10+
- Node.js 18+
- npm 9+

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd administradorNegocios
```

### 2. Configurar el backend (FastAPI)

```bash
# Entrar al directorio del backend
cd backend

# Crear y activar el entorno virtual
python -m venv .venv

# En Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Levantar el servidor de desarrollo
uvicorn app.main:app --reload
```

El backend FastAPI queda disponible en `http://localhost:8000`.

### 3. Configurar el backend Django (legacy)

```bash
# Entrar al directorio del proyecto Django
cd backend/ventaDiariosBack

# Crear y activar el entorno virtual
python -m venv venv

# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install django djangorestframework django-cors-headers Pillow

# Aplicar las migraciones
python manage.py migrate

# (Opcional) Crear un superusuario para el panel de admin
python manage.py createsuperuser

# Levantar el servidor de desarrollo
python manage.py runserver
```

El backend Django queda disponible en `http://localhost:8000` (correr uno u otro, no ambos en el mismo puerto).

### 4. Configurar el frontend

Abrí una nueva terminal desde la raíz del proyecto:

```bash
# Desde la raíz del proyecto
npm install

# Levantar el servidor de desarrollo
npm run dev
```

El frontend queda disponible en `http://localhost:5173`.

---

## Uso

1. Con ambos servidores corriendo, abrí `http://localhost:5173` en el navegador.
2. Desde la interfaz podés:
   - **Ventas del día**: registrar los diarios vendidos con nombre y precio.
   - **Inventario**: agregar productos con código de barras y actualizar su stock y ventas.
   - **Devoluciones**: subir una foto de la mercadería devuelta junto con la fecha.
3. La API también puede consumirse directamente desde herramientas como Postman o curl usando los endpoints documentados arriba.
4. El panel de administración de Django está disponible en `http://localhost:8000/admin/` (requiere superusuario).
