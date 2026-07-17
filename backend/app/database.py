"""Configuración de la conexión a base de datos con SQLAlchemy.

Provee el engine, la sesión y la base declarativa para los modelos.
Usa la DATABASE_URL definida en config.py (SQLite en dev, Postgres en prod).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# SQLite requiere check_same_thread=False para FastAPI (multithread)
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=(settings.app_env == "local"),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos SQLAlchemy."""
    pass


def get_db():
    """Generador de sesiones para inyección de dependencias en FastAPI.

    Yields:
        Session: Sesión activa de SQLAlchemy.

    Asegura que la sesión se cierre al finalizar el request.
    """
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()
