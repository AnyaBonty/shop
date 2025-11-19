from uuid import uuid4

from jose import jwt, JWTError

from backend.app.core.config import settings
from datetime import datetime, timedelta,timezone

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS



def create_access_token(data: dict):
    to_encode = data.copy()
    """Создаёт JWT access token (короткий срок). subject обычно user_id."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp": expire})
    token= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise e

