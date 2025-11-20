from uuid import uuid4

from jose import jwt, JWTError

from backend.app.core.config import settings
from datetime import datetime, timedelta,timezone
from backend.app.core.redis import redis, add_token_to_redis, check_token_in_redis

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS



async def create_access_token(data: dict):
    to_encode = data.copy()
    """Создаёт JWT access token (короткий срок)."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp": expire})
    token= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # TTL в секундах
    ttl = int((expire - datetime.now(timezone.utc)).total_seconds())
    await add_token_to_redis(token,ttl)

    return token


'''
def create_refresh_token(subject: str, role:str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=refresh_token_expire_days)
    jti=str(uuid4())
    to_encode = {
        "sub": str(subject),
        "role": role,
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int(expire.timestamp()),
        "jti": jti  # уникальный id токена (может пригодиться)
    }
    token= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token, "jti": jti, "exp": to_encode["exp"]}
'''


async def decode_access_token(token: str):
    try:
        await check_token_in_redis(token)

        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise e

