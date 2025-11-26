# app/cactuspay.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

CACTUSPAY_TOKEN = os.getenv("CACTUSPAY_TOKEN")
BASE_URL = "https://lk.cactuspay.pro/api/?method="


async def cactuspay_create_payment(order_id: str, amount: float, description: str, method: str):
    """
    Создание платежа CactusPay
    """
    payload = {
        "token": CACTUSPAY_TOKEN,
        "order_id": order_id,
        "amount": amount,
        "description": description,
        "method": method,
        "h2h": False
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(BASE_URL + "create", json=payload)
        return r.json()


async def cactuspay_get_status(order_id: str):
    """
    Проверка статуса платежа
    """
    payload = {
        "token": CACTUSPAY_TOKEN,
        "order_id": order_id
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(BASE_URL + "get", json=payload)
        return r.json()
