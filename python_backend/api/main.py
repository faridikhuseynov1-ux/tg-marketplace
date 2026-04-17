import os
import hmac
import hashlib
import json
from urllib.parse import unquote
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List

from python_backend.db.database import get_db
from python_backend.db.models import Item, User, ItemStatus, Transaction

app = FastAPI(title="P2P Marketplace API")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "12345:DUMMY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ItemResponse(BaseModel):
    id: int
    title: str
    price: float
    category: str
    image: str
    class Config: from_attributes = True

class CheckoutRequest(BaseModel):
    action: str
    itemId: int
    price: float
    source: str

def validate_telegram_data(init_data: str, token: str) -> bool:
    """Криптографическая проверка подлинности данных от Telegram Web App"""
    try:
        parsed_data = dict(qc.split("=") for qc in unquote(init_data).split("&"))
        received_hash = parsed_data.pop("hash", None)
        if not received_hash:
            return False
            
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
        secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        return calculated_hash == received_hash
    except Exception:
        return False

def verify_telegram_user(authorization: str = Header(None)):
    """Авторизация и извлечение данных пользователя"""
    if not authorization or not authorization.startswith("tma "):
        # Заглушка для локальных тестов браузера
        return {"id": 111222333, "username": "system_seller"} 
        
    init_data = authorization.split(" ")[1]
    if not validate_telegram_data(init_data, TELEGRAM_BOT_TOKEN):
        raise HTTPException(status_code=403, detail="Forbidden: Ошибка подписи Telegram")
        
    parsed_data = dict(qc.split("=") for qc in unquote(init_data).split("&"))
    try:
        user_data = json.loads(unquote(parsed_data.get("user", "{}")))
        return user_data
    except Exception:
        return {"id": 111222333, "username": "system_seller"}

@app.get("/api/v1/items", response_model=List[ItemResponse])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.status == ItemStatus.ACTIVE))
    items = result.scalars().all()
    return [
        ItemResponse(
            id=i.id, title=i.title, price=float(i.price),
            category="Premium" if "Premium" in i.title else "Digital Trade",
            image="https://cdn-icons-png.flaticon.com/512/2111/2111646.png"
        ) for i in items
    ]

# === УЛУЧШЕНИЕ SENIOR УРОВНЯ: ТРАНЗАКЦИОННАЯ ESCROW ЛОГИКА ===
@app.post("/api/v1/checkout")
async def process_checkout(req: CheckoutRequest, db: AsyncSession = Depends(get_db), tg_user: dict = Depends(verify_telegram_user)):
    item = await db.get(Item, req.itemId)
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден в базе")
        
    if item.status != ItemStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Товар уже продан или зарезервирован")
        
    # Синхронизация данных с таблицей юзеров
    res = await db.execute(select(User).where(User.telegram_id == tg_user.get("id")))
    user = res.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Профиль не найден. Авторизуйтесь через бота (/start).")
        
    if float(user.balance) < float(item.price):
        raise HTTPException(status_code=400, detail=f"Недостаточно средств. Ваш баланс: ${user.balance:.2f}")
        
    # Блокировка баланса (Escrow механика вычета)
    user.balance = float(user.balance) - float(item.price)
    item.status = ItemStatus.PENDING # Товар замораживается на время сделки
    
    # Запись в Transaction Log
    tx = Transaction(user_id=user.id, amount=-item.price, tx_type="ESCROW_HOLD_BUY")
    db.add(tx)
    
    await db.commit() # Сохраняем состояние
    
    return {
        "status": "success", 
        "message": f"Сделка Escrow на '{item.title}' оформлена! Заморожено ${item.price:.2f}", 
        "deducted": float(item.price)
    }
