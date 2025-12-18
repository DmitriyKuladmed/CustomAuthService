"""
Утилиты для работы с JWT токенами
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from typing import Dict, Optional


def generate_access_token(user_id: str) -> str:
    """Генерация access токена"""
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def generate_refresh_token(user_id: str) -> str:
    """Генерация refresh токена"""
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        "iat": datetime.utcnow(),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[Dict]:
    """Декодирование и валидация JWT токена"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """Извлечение user_id из токена"""
    payload = decode_token(token)
    if payload and payload.get("type") == "access":
        return payload.get("user_id")
    return None


