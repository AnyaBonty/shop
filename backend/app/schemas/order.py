from pydantic import BaseModel
from datetime import datetime

from .product import ProductRead

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class OrderItemRead(OrderItemBase):
    product: ProductRead

class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    items: list[OrderItemBase]

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    items: list[OrderItemRead]

