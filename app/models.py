from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    user_id = Column(String)
    recipient = Column(String)
    product = Column(String)
    amount_rub = Column(Float)
    currency = Column(String)
    status = Column(String, default="pending")
    invoice_id = Column(String, nullable=True)
    type_of_payment = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
