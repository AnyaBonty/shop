import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from sqlalchemy.orm import selectinload

from backend.app.models import Order, OrderItem, Product
from backend.app.schemas.order import OrderRead, OrderItemRead, OrderCreate, OrderUpdate, OrdersRead, OrderItemBase


async def get_order(db: AsyncSession, order_id: int):
    stmt = select(Order).where(Order.id == order_id).options(
        selectinload(Order.items).selectinload(OrderItem.product))  # подгрузка с зависимыми таблицами
    read_order = await db.execute(stmt)
    result_order = read_order.scalar_one_or_none()
    if result_order is None:
        return None
    return result_order

async def get_order_by_id(db: AsyncSession, order_id: int):
    read_order= await get_order(db, order_id)
    if read_order is None:
        return None
    return OrderRead.model_validate(read_order)


async def get_order_by_user(db: AsyncSession, user_id: int):
    read_orders=await db.execute(
        select(Order).where(Order.user_id == user_id).
        options(selectinload(Order.items).selectinload(OrderItem.product)))
    if read_orders is None:
        return None
    res=read_orders.scalars().all()

    result_list=[]
    for order in res:
        result_list.append(OrderRead.model_validate(order))

    result=OrdersRead(list_orders=result_list)
    return result



async def create_items(db: AsyncSession,order_id:int, items: list[OrderItemBase]):
    total_price = 0
    for item in items:
        product = await db.execute(select(Product.price).where(Product.id == item.product_id))
        price_product = product.scalar_one_or_none()
        if price_product is None:
            return None
        db_item = OrderItem(order_id=order_id, product_id=item.product_id, quantity=item.quantity,
                            price=price_product * item.quantity)

        total_price = total_price + db_item.price

        db.add(db_item)

    return total_price

async def create_order(db: AsyncSession, order: OrderCreate):
    new_order = Order(created_at=datetime.now(timezone.utc),user_id=order.user_id)
    db.add(new_order)
    await db.flush()  # получаем new_order.id из базы без commit

    total_price = await create_items(db,new_order.id,order.items)

    new_order.price = total_price


    await db.commit()
    await db.refresh(new_order)

    result=await get_order_by_id(db, new_order.id)

    return result



async def update_order(db: AsyncSession,order_id:int, order_update: OrderUpdate):
    old_order = await get_order(db, order_id)
    if old_order is None:
        return None


    #Обновляем юзера, если его изменили не на None
    if old_order.user_id != order_update.user_id and order_update.user_id:

        old_order.user_id = order_update.user_id

    if order_update.items:
        # Удаляем старые
        for item in old_order.items:
            await db.delete(item)

    old_order.price = await create_items(db,old_order.id,order_update.items)

    await db.commit()

    result=await get_order_by_id(db, old_order.id)
    if result is None:
        return None
    return result


