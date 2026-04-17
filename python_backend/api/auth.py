import jwt
import os
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("TELEGRAM_BOT_TOKEN", "12345:DUMMY")

def create_jwt_token(data: dict):
    """Генерация безопасного JWT токена"""
    to_encode = data.copy()
    # Токен живет 7 дней, после чего юзеру придется переоткрыть WebApp
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def decode_jwt_token(token: str):
    """Расшифровка токена и возврат payload (словаря)"""
    try:
        decoded_data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return decoded_data
    except Exception:
        return None
