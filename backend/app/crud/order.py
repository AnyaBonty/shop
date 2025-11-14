import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from sqlalchemy.orm import selectinload

from backend.app.models import Order,OrderItem
from backend.app.schemas.order import OrderRead, OrderItemRead, OrderCreate


async def get_order_by_id(db: AsyncSession, order_id: int):
    stmt=select(Order).where(Order.id == order_id).options(selectinload(Order.items).selectinload(OrderItem.product)) #подгрузка с зависимыми таблицами
    read_order= await db.execute(stmt)
    result_order=read_order.scalar_one_or_none()
    if result_order is None:
        return None

    return OrderRead.model_validate(result_order)

async def create_order(db: AsyncSession, order: OrderCreate):
    new_order = Order(created_at=datetime.now(timezone.utc),user_id=order.user_id)
    db.add(new_order)
    await db.flush()  # получаем new_order.id из базы без commit

    for item in order.items:
        item=OrderItem(order_id=new_order.id,product_id=item.product_id,quantity=item.quantity)
        db.add(item)

    await db.commit()

    result=await get_order_by_id(db, new_order.id)
    if result is None:
        return None

    return result
