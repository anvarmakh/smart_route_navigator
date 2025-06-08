# ✅ celery_worker.py — запускает Celery worker с настройками из .env
from celery import Celery
import os
from dotenv import load_dotenv

# 📊 Загружаем переменные окружения из .env файла
load_dotenv()

# 👀 Получаем URL брокера и backend для Redis из .env
broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend_url = os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/0")

# 🛠️ Инициализируем Celery
celery_app = Celery(
    "smart_route_tasks",
    broker=broker_url,
    backend=backend_url
)

# 🔍 Автоматический поиск задач в модуле app.tasks
celery_app.autodiscover_tasks(["app.tasks"])
