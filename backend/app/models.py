from __future__ import annotations #откладывать создание аннотации типов нужно откладывать
from sqlalchemy import Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from backend.app.db.base import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    email: Mapped[str| None] = mapped_column(String(70), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), index=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, default=0)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)

    order_items: Mapped[list["OrderItem"]]=relationship(back_populates='product')


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items: Mapped[list["OrderItem"]]=relationship(back_populates='order', cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    order: Mapped[Order] = relationship(back_populates='items')
    product: Mapped[Product] = relationship(back_populates='order_items')
