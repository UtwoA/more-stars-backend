from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import os, datetime, uuid, httpx
from .database import SessionLocal, Base, engine
from .models import Order
from .crypto import convert_to_rub

load_dotenv()
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")  # твой testnet токен
CRYPTO_PAY_API_URL = "https://testnet-pay.crypt.bot/api/createInvoice"

app = FastAPI()
Base.metadata.create_all(bind=engine)


class OrderCreate(BaseModel):
    user_id: str
    recipient: str
    product: str
    amount: float
    currency: str  # TON / USDT


async def create_crypto_invoice(amount: float, currency: str, order_id: str, recipient: str):
    payload = {
        "currency_type": "crypto",        # тип платежа
        "asset": currency.upper(),        # криптовалюта
        "amount": amount,                 # сумма
        "description": f"Покупка {recipient}",
        "payload": order_id,
        "allow_comments": False,
        "allow_anonymous": False
    }
    headers = {
        "Crypto-Pay-API-Token": CRYPTOBOT_TOKEN,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(CRYPTO_PAY_API_URL, json=payload, headers=headers, timeout=15)
        return r.json()


@app.post("/create_order")
async def create_order(order: OrderCreate):
    amount_rub = await convert_to_rub(order.currency, order.amount)
    db = SessionLocal()
    order_id = str(uuid.uuid4())
    db_order = Order(
        order_id=order_id,
        user_id=order.user_id,
        recipient=order.recipient if order.recipient != "@unknown" else "self",
        product=order.product,
        amount_rub=amount_rub,
        currency=order.currency,
        status="created",
        type_of_payment="crypto",
        timestamp=datetime.datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # создаём инвойс в Crypto Pay Testnet
    invoice = await create_crypto_invoice(order.amount, order.currency, order_id, db_order.recipient)

    db.close()
    return {
        "order_id": order_id,
        "amount_rub": amount_rub,
        "crypto_invoice": invoice  # тут будет JSON с ссылкой на оплату
    }


@app.post("/webhook/crypto")
async def crypto_webhook(request: Request):
    data = await request.json()
    db = SessionLocal()
    order = db.query(Order).filter(Order.order_id == data.get("order_id")).first()
    if order:
        order.status = data.get("status", order.status)
        db.commit()
    db.close()
    return {"status": "ok"}
