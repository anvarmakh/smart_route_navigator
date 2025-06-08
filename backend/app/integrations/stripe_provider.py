# Работа с платёжной системой Stripe (создание сессий, Webhook)
import stripe

stripe.api_key = "your_stripe_secret_key"

def create_checkout_session(user_id: int, price_id: str):
    """
    Создаёт сессию Stripe Checkout для оформления подписки
    """
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url="https://yourapp.com/success",
        cancel_url="https://yourapp.com/cancel",
        metadata={"user_id": user_id}
    )
    return session.url

def handle_stripe_event(event):
    """
    Обработка webhook от Stripe для событий подписки
    """
    if event["type"] == "checkout.session.completed":
        user_id = event["data"]["object"]["metadata"]["user_id"]
        # Здесь можно обновить статус подписки в базе данных
        print(f"Пользователь {user_id} успешно оформил подписку")
