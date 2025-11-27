import uuid
import os
import logging
import httpx
from dotenv import load_dotenv

from .models import Order
from .database import SessionLocal


dotenv_path = "/var/www/crypto_mvp/more-stars-backend/.env"
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger("robynhood")

ROBYNHOOD_API_URL = os.getenv("ROBYNHOOD_TEST_API_URL", "https://robynhood.parssms.info/api/test/purchase")
ROBYNHOOD_API_TOKEN = os.getenv("ROBYNHOOD_API_TOKEN")


import re

async def send_purchase_to_robynhood(order):
    idempotency_key = str(uuid.uuid4())

    # Преобразуем product для API
    product_type = order.product.lower()  # "stars", "premium", "ads" — пусть приходит в order.product
    payload = {
        "product_type": product_type,
        "recipient": order.recipient,
        "idempotency_key": idempotency_key
    }

    # Достаем числовое значение из строки (например, "50 ⭐" → 50)
    if product_type == "stars":
        payload["quantity"] = int(re.sub(r"\D", "", order.product))  # оставляем только цифры
    elif product_type == "premium":
        payload["months"] = int(re.sub(r"\D", "", order.product))
    elif product_type == "ads":
        payload["amount"] = int(re.sub(r"\D", "", order.product))

    headers = {
        "X-API-Key": ROBYNHOOD_API_TOKEN,
        "Content-Type": "application/json"
    }

    logger.info(f"[ROBYNHOOD] Sending: {payload}")

    async with httpx.AsyncClient() as client:
        r = await client.post(ROBYNHOOD_API_URL, json=payload, headers=headers, timeout=15)
        resp = r.json()
        logger.info(f"[ROBYNHOOD] Response: {resp}")

    # сохраняем idempotency_key
    db = SessionLocal()
    db_order = db.query(Order).filter(Order.order_id == order.order_id).first()
    if db_order:
        db_order.idempotency_key = idempotency_key
        db.commit()
    db.close()

    return resp

