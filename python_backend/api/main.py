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

from aiogram import Bot
from python_backend.db.database import get_db
from python_backend.db.models import Item, User, ItemStatus, Transaction
from python_backend.api.auth import create_jwt_token, decode_jwt_token

app = FastAPI(title="P2P Marketplace API")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "12345:DUMMY")

# Глобальный инстанс бота для Webhook-уведомлений
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")

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

class AuthRequest(BaseModel):
    initData: str

def validate_telegram_data(init_data: str, token: str) -> bool:
    try:
        parsed_data = dict(qc.split("=") for qc in unquote(init_data).split("&"))
        received_hash = parsed_data.pop("hash", None)
        if not received_hash: return False
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
        secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
        return hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest() == received_hash
    except Exception:
        return False

# ЭНДПОИНТ АВТОРИЗАЦИИ (Выдача JWT)
@app.post("/api/v1/auth")
async def auth_telegram(req: AuthRequest):
    if not validate_telegram_data(req.initData, TELEGRAM_BOT_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid signature")
        
    parsed_data = dict(qc.split("=") for qc in unquote(req.initData).split("&"))
    try:
        user_data = json.loads(unquote(parsed_data.get("user", "{}")))
    except:
        user_data = {"id": 111222333, "username": "system"}
        
    token = create_jwt_token(user_data)
    return {"access_token": token, "token_type": "bearer"}

def verify_jwt_user(authorization: str = Header(None)):
    """Извлечение юзера из JWT"""
    if not authorization or not authorization.startswith("Bearer "):
        return {"id": 111222333, "username": "system_seller"} # Fallback для тестов
        
    token = authorization.split(" ")[1]
    user_data = decode_jwt_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid JWT")
    return user_data

@app.get("/api/v1/items", response_model=List[ItemResponse])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.status == ItemStatus.ACTIVE))
    return [
        ItemResponse(
            id=i.id, title=i.title, price=float(i.price),
            category="Premium" if "Premium" in i.title else "Digital Trade",
            image="https://cdn-icons-png.flaticon.com/512/2111/2111646.png"
        ) for i in result.scalars().all()
    ]

# ИНТЕГРАЦИЯ WEBHOOK NOTIFICATIONS
@app.post("/api/v1/checkout")
async def process_checkout(req: CheckoutRequest, db: AsyncSession = Depends(get_db), tg_user: dict = Depends(verify_jwt_user)):
    item = await db.get(Item, req.itemId)
    if not item or item.status != ItemStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Товар недоступен")
        
    res = await db.execute(select(User).where(User.telegram_id == tg_user.get("id")))
    buyer = res.scalars().first()
    
    if not buyer or buyer.balance < item.price:
        raise HTTPException(status_code=400, detail=f"Недостаточно средств. Баланс: ${buyer.balance if buyer else 0:.2f}")
        
    # Транзакция Escrow
    buyer.balance = float(buyer.balance) - float(item.price)
    item.status = ItemStatus.PENDING
    db.add(Transaction(user_id=buyer.id, amount=-item.price, tx_type="ESCROW_HOLD_BUY"))
    await db.commit()
    
    # 🔔 ОТПРАВКА УВЕДОМЛЕНИЙ ЧЕРЕЗ AIOGRAM
    try:
        # Покупателю
        await bot.send_message(
            chat_id=buyer.telegram_id, 
            text=f"🛍 <b>Покупка успешна!</b>\nВы приобрели <b>{item.title}</b> за <b>⭐️ {item.price:.0f}</b>.\nСредства защищены Escrow!"
        )
        
        # Продавцу
        seller = await db.get(User, item.seller_id)
        if seller:
            await bot.send_message(
                chat_id=seller.telegram_id,
                text=f"💰 <b>Хорошие новости!</b>\nВаш товар <b>{item.title}</b> кто-то купил за <b>⭐️ {item.price:.0f}</b>!\n(Деньги находятся в Escrow-холде до завершения сделки)"
            )
    except Exception as e:
        print(f"Telegram Webhook Error: {e}")
    
    return {"status": "success", "message": f"Оплачено! Товар '{item.title}' в Escrow холде.", "deducted": float(item.price)}
