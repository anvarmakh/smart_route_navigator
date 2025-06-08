import os
import smtplib
from email.message import EmailMessage
import requests

# ✉️ Простая email-рассылка для админов (через SMTP)
def notify_admin_via_email(subject: str, message: str):
    """
    Отправляет email администратору с использованием SMTP.
    Значения берутся из переменных окружения:
    - ADMIN_EMAIL
    - SMTP_SERVER
    - SMTP_PORT (по умолчанию 587)
    - SMTP_USER / SMTP_PASS

    На проде лучше использовать внешние сервисы: SendGrid, Mailgun, SES.
    """
    admin_email = os.getenv("ADMIN_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not all([admin_email, smtp_server, smtp_user, smtp_pass]):
        print("[WARN] Email config is incomplete.")
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = admin_email
        msg.set_content(message)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print("[INFO] Alert email sent to admin.")
    except Exception as e:
        print("[ERROR] Failed to send email:", e)

# 📲 Telegram уведомление для админа через бота
def notify_admin_via_telegram(message: str):
    """
    Отправляет уведомление администратору в Telegram через бота.
    Требует в .env:
    - TELEGRAM_BOT_TOKEN
    - TELEGRAM_CHAT_ID
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("[WARN] Telegram config missing")
        return

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("[INFO] Telegram alert sent.")
        else:
            print("[ERROR] Telegram alert failed:", response.text)
    except Exception as e:
        print("[ERROR] Telegram exception:", e)

# 🚨 Унифицированная функция для отправки оповещений во все каналы
def notify_all_channels(subject: str, message: str):
    """
    Отправляет уведомление по всем доступным каналам: email + Telegram.
    """
    notify_admin_via_email(subject, message)
    notify_admin_via_telegram(message)