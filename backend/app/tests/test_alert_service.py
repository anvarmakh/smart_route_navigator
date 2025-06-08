# ✅ Тесты для alert_service

import pytest
from unittest.mock import patch
from app.services.alert_service import notify_admin_via_email, notify_admin_via_telegram
import os

# 🔧 Предустановки для окружения
def setup_module(module):
    os.environ["ADMIN_EMAIL"] = "admin@example.com"
    os.environ["SMTP_SERVER"] = "smtp.example.com"
    os.environ["SMTP_USER"] = "noreply@example.com"
    os.environ["SMTP_PASS"] = "password123"
    os.environ["TELEGRAM_BOT_TOKEN"] = "dummy_token"
    os.environ["TELEGRAM_CHAT_ID"] = "123456789"

# ✅ Тест email-уведомления
@patch("smtplib.SMTP")
def test_notify_admin_via_email(mock_smtp):
    notify_admin_via_email("Test Subject", "Test Message")
    instance = mock_smtp.return_value.__enter__.return_value
    instance.send_message.assert_called_once()

# ✅ Тест telegram-уведомления
@patch("requests.post")
def test_notify_admin_via_telegram(mock_post):
    mock_post.return_value.status_code = 200
    notify_admin_via_telegram("Hello Telegram")
    mock_post.assert_called_once()

# ✅ Тест: Telegram выключен (без переменных окружения)
def test_telegram_disabled(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    notify_admin_via_telegram("Silent mode")  # Должно пройти без ошибки