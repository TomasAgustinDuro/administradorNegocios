"""Configuración centralizada de la aplicación.

Lee variables de entorno y provee valores por defecto para desarrollo.
En producción, setear DATABASE_URL apuntando a PostgreSQL.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración global leída desde variables de entorno."""

    app_env: str = "local"
    app_port: int = 8000
    database_url: str = "sqlite:///./dev.db"
    cors_origins: str = "http://localhost:5173"

    def get_cors_origins_list(self) -> list[str]:
        """Convierte el string de origins a una lista."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
