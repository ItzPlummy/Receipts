from datetime import datetime
from enum import StrEnum

from sqlalchemy import Column, UUID, func, String, DateTime, Numeric, Enum, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class PaymentType(StrEnum):
    CASH = "cash"
    CASHLESS = "cashless"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(True), primary_key=True, server_default=func.gen_random_uuid())
    username = Column(String(), unique=True, nullable=False)
    email = Column(String(), unique=True, nullable=False)
    password_hash = Column(String(), nullable=False)

    created_at = Column(DateTime(), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(), nullable=True, onupdate=datetime.now)

    receipts = relationship("Receipt", back_populates="user")


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(UUID(True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(UUID(True), ForeignKey("users.id"), nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    payment_amount = Column(Numeric(), nullable=False)
    total = Column(Numeric(), nullable=False)
    rest = Column(Numeric(), nullable=False)

    created_at = Column(DateTime(), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(), nullable=True, onupdate=datetime.now)

    user = relationship("User", back_populates="receipts")
    products = relationship("Product", back_populates="receipt")


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(True), primary_key=True, server_default=func.gen_random_uuid())
    receipt_id = Column(UUID(True), ForeignKey("receipts.id"), nullable=False)
    name = Column(String(), nullable=False)
    price = Column(Numeric(), nullable=False)
    quantity = Column(Integer(), nullable=False)
    total = Column(Numeric(), nullable=False)

    created_at = Column(DateTime(), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(), nullable=True, onupdate=datetime.now)

    receipt = relationship("Receipt", back_populates="products")
