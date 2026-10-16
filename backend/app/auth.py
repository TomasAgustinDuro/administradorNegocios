import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthenticationCredentials, HTTPBearer


def verify_token(credentials: HTTPAuthenticationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials

    try:
        secret = os.getenv("JWT_SECRET")
        jwt.decode(token, secret, algorithms=["HS256"])
        return True
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token Inválido")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token Inválido")
