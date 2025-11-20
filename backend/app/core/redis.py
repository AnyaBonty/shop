from fastapi import HTTPException,status
from redis.asyncio import Redis
from backend.app.core.config import settings

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def add_token_to_redis(token: str, expire_seconds: int):
    """Добавляем токен в Redis с TTL"""
    await redis.set(token, "active", ex=expire_seconds)

async def remove_token_from_redis(token: str):
    """Удаляем токен из Redis при logout"""
    await redis.delete(token)

async def check_token_in_redis(token: str):
    """Проверяем, что токен есть и активен"""
    value = await redis.get(token)
    if value is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен не найден")

