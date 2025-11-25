from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from .database import Base, engine, SessionLocal
from .models import Order
from .crypto_pay import create_invoice, verify_signature
from .binance import convert_to_rub
import uuid

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/webhook/crypto")
async def crypto_webhook(request: Request, crypto_pay_api_signature: str = Header(...)):
    body = await request.body()

    if not verify_signature(body, crypto_pay_api_signature):
        return JSONResponse(status_code=400, content={"message": "Invalid signature"})

    data = await request.json()
    invoice_id = data.get("invoice_id")
    order_payload = data.get("payload")  # order_id
    status = data.get("status")
    paid_asset = data.get("paid_asset")
    paid_amount = float(data.get("paid_amount", 0))

    amount_rub = convert_to_rub(paid_asset, paid_amount)

    db = SessionLocal()
    order = db.query(Order).filter(Order.order_id == order_payload).first()
    if order:
        order.status = status
        order.amount_rub = amount_rub
        order.invoice_id = invoice_id
        db.commit()
    db.close()

    return {"ok": True}


@app.post("/create_order")
async def create_order(order: dict):
    """
    Создаем заказ + инвойс в Crypto Pay
    """
    db = SessionLocal()
    order_id = str(uuid.uuid4())
    recipient = order.get("recipient") or "self"

    db_order = Order(
        order_id=order_id,
        user_id=order.get("id"),
        recipient=recipient,
        product=order.get("title"),
        amount_rub=float(order.get("price", 0)),
        currency="RUB",
        type_of_payment="crypto",
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    invoice = create_invoice(db_order.amount_rub, "RUB", order_id, recipient)

    db_order.invoice_id = invoice.get("invoice_id")
    db.commit()
    db.close()

    return {"order_id": order_id, "invoice": invoice}
