from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Product
from backend.app.schemas.product import *


async def get_product_by_id(db:AsyncSession, id:int):
    read_product=await db.execute(select(Product).where(Product.id==id))
    return read_product.scalar_one_or_none()

async def get_product_by_name(db:AsyncSession, name:str):
    read_product=await db.execute(select(Product).where(Product.name==name))
    return read_product.scalar_one_or_none()


async def create_product(db:AsyncSession, product:ProductCreate):
    new_item= Product(name=product.name,description=product.description,
                      price=product.price, image_url=product.image_url)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return ProductRead.model_validate(new_item)

async def delete_product(db:AsyncSession, id:int):
    product=await get_product_by_id(db, id)
    if not product:
        return None
    await db.delete(product)
    await db.commit()
    await db.refresh(product)
    return product

async def update_product(db:AsyncSession, id:int, new_product:ProductUpdate):
    product=await get_product_by_id(db, id)
    if not product:
        return None
    product.name=new_product.name
    product.description=new_product.description
    product.price=new_product.price
    product.image_url=new_product.image_url
    await db.commit()
    await db.refresh(product)
    return product

async def search_products_by_name(db:AsyncSession, name_part:str):
    search_products=await db.execute(select(Product).where(Product.name.ilike(f"%{name_part}%"))) #Поиск продуктов, где частью названия является запрос без учета регистра
    if not search_products:
        return None
    return search_products.scalars().all()


