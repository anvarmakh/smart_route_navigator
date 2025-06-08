# Логирование всех HTTP-запросов и ответов
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("smart_route")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response