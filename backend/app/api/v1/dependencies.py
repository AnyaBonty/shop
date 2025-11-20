from fastapi import Depends,Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from backend.app.core.config import settings
from backend.app.core.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

'''
async def get_token(authorization: str = Header(..., alias="Authorization")):
    """Проверяем заголовок Authorization: Bearer <token>"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    return token
'''
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Декодируем токен и возвращаем данные пользователя"""
    try:
        payload = decode_access_token(token)
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token")
        return {"user_id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")