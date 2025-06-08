# Извлечение пользователя из JWT и сохранение в request.state.user
from fastapi import Request, HTTPException
from app.services.auth_service import decode_access_token

async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        try:
            payload = decode_access_token(token[7:])
            request.state.user = {"email": payload["sub"], "subscription": "premium"}  # Условный пример
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        request.state.user = {"subscription": "basic"}  # Гость
    return await call_next(request)
