from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.routes import routing
from app.api.v1.routes import history as history_router
from app.api.v1.auth import router as auth_router
from app.services.auth_service import auth_middleware
from app.middlewares.logging_middleware import LoggingMiddleware

app = FastAPI()

# Middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(LoggingMiddleware)
app.middleware("http")(auth_middleware)

# Роуты
app.include_router(routing.router, prefix="/api/v1")  # маршруты для маршрутизации и карты
app.include_router(auth_router)  # авторизация, регистрация, профиль трака
app.include_router(history_router.router, prefix="/api/v1")