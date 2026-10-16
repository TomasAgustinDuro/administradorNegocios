"""Generador de tokens JWT para desarrollo y testing.

Script utilitario que genera un token JWT válido para autenticarse
en los endpoints protegidos (POST, PUT, DELETE).

Uso:
    python generate_token.py

El token se imprime en stdout y puede copiarse para usarlo
en headers Authorization: Bearer <token>
"""

import jwt
import os
from datetime import datetime, timedelta

# Lee el secret desde variables de entorno o usa el default
SECRET_KEY = os.getenv("JWT_SECRET", "administrador-negocios-portfolio-2024")

# Datos del token
payload = {
    "user": "admin",
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow() + timedelta(hours=24),
}

# Genera el token
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("=" * 80)
print("TOKEN JWT GENERADO (válido por 24 horas)")
print("=" * 80)
print(f"\n{token}\n")
print("=" * 80)
print("CÓMO USAR:")
print("=" * 80)
print("\n1. Con curl:")
print(f'   curl -X POST http://localhost:8000/api/v1/products \\')
print(f'     -H "Authorization: Bearer {token}" \\')
print(f'     -H "Content-Type: application/json" \\')
print(f'     -d \'{{"name": "Laptop", "price": 1000, "quantity": 5}}\'')
print("\n2. Con Postman:")
print("   - Tab 'Authorization'")
print("   - Type: Bearer Token")
print(f"   - Token: {token}")
print("\n3. Probar SIN token (debe fallar con 401):")
print(f'   curl -X POST http://localhost:8000/api/v1/products \\')
print(f'     -H "Content-Type: application/json" \\')
print(f'     -d \'{{"name": "Laptop", "price": 1000, "quantity": 5}}\'')
print("\n" + "=" * 80)
