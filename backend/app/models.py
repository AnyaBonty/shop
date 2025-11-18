from __future__ import annotations #откладывать создание аннотации типов нужно откладывать
from sqlalchemy import Integer, String, Boolean, Float, ForeignKey,TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime,timezone


from backend.app.db.base import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    first_name: Mapped[String] = mapped_column(String(50),nullable=True)
    last_name: Mapped[String] = mapped_column(String(50),nullable=True)
    email: Mapped[str| None] = mapped_column(String(70), unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=True,default=1)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

    orders: Mapped[list['Order']] = relationship(back_populates='users', cascade='all, delete-orphan')
    role: Mapped['Role'] = relationship(back_populates='users')


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str|None] = mapped_column(String(100), nullable=True)

    users: Mapped[list['User']] = relationship(back_populates='role')


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
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    price: Mapped[float] = mapped_column(Float, default=0)

    items: Mapped[list["OrderItem"]]=relationship(back_populates='order', cascade="all, delete-orphan")
    users: Mapped['User']=relationship(back_populates='orders')


class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price: Mapped[float] = mapped_column(Float, default=0, nullable=True)

    order: Mapped[Order] = relationship(back_populates='items')
    product: Mapped[Product] = relationship(back_populates='order_items')

