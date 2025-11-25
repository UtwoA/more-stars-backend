import os
import hmac
import hashlib
import httpx
from dotenv import load_dotenv

load_dotenv()

CRYPTO_PAY_API_URL = "https://testnet-pay.crypt.bot/v1/invoice"
API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN")  # твой токен


def create_invoice(amount: float, currency: str, order_id: str, recipient: str):
    """
    Создаем инвойс в Crypto Pay API
    """
    payload = {
        "amount": amount,
        "currency": currency,
        "payload": order_id,
        "description": f"Покупка {recipient}",
        "allow_comments": False,
        "allow_anonymous": False
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = httpx.post(CRYPTO_PAY_API_URL, json=payload, headers=headers)
    return response.json()


def verify_signature(request_body: bytes, signature: str):
    """
    Проверка HMAC подписи вебхука
    """
    secret = API_TOKEN.encode()
    computed_signature = hmac.new(secret, request_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_signature, signature)
