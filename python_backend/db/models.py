from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from python_backend.db.database import Base

class ItemStatus(PyEnum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SOLD = "SOLD"
    BANNED = "BANNED"

class AdType(PyEnum):
    BUY = "BUY"
    SELL = "SELL"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    balance = Column(Numeric(10, 2), default=0.00, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("Item", back_populates="seller")
    ads = relationship("Ad", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(ItemStatus), default=ItemStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    seller = relationship("User", back_populates="items")

class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=True)
    type = Column(Enum(AdType), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="ads")
    item = relationship("Item")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    tx_type = Column(String, nullable=False) # DEPOSIT, WITHDRAW, PURCHASE, HOLD
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="transactions")
