import os
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from sqlalchemy.future import select

from python_backend.db.database import AsyncSessionLocal
from python_backend.db.models import User, Transaction

user_router = Router()

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Генерация базовой Reply-клавиатуры для пользователя"""
    kb = [
        [KeyboardButton(text="📱 Магазин"), KeyboardButton(text="💰 Баланс")],
        [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="ℹ️ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = res.scalars().first()
        if not user:
            # Senior Фича: Каждому новому юзеру выдаем стартовые $100.00 для тестов системы покупок!
            new_user = User(telegram_id=message.from_user.id, username=message.from_user.username, balance=100.00)
            db.add(new_user)
            await db.commit()
            
            await message.answer(
                f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
                f"🎉 В честь регистрации мы начислили вам бонус: <b>$100.00</b>!\n"
                f"Откройте [📱 Магазин] и совершите свою первую безопасную покупку.",
                reply_markup=get_main_keyboard(),
                parse_mode="HTML"
            )
            return

    await message.answer(
        f"С возвращением, <b>{message.from_user.first_name}</b>!\nВыбери нужный раздел в нижнем меню 👇",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )

@user_router.message(F.text == "📱 Магазин")
async def process_shop_button(message: Message):
    web_app_url = os.getenv("WEB_APP_URL", "https://t.me/durov")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Открыть маркетплейс", web_app=WebAppInfo(url=web_app_url))]
    ])
    await message.answer("Каталог защищенных покупок: 🛒", reply_markup=markup)

@user_router.message(F.text == "💰 Баланс")
async def process_balance_button(message: Message):
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = res.scalars().first()
        balance = user.balance if user else 0.00
    
    await message.answer(f"💰 Доступно: <b>${balance}</b>", parse_mode="HTML")

# === УЛУЧШЕНИЕ SENIOR УРОВНЯ: ДЕТАЛЬНЫЙ ПРОФИЛЬ С ТРАНЗАКЦИЯМИ ===
@user_router.message(F.text == "👤 Профиль")
async def process_profile_button(message: Message):
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = res.scalars().first()
        
        if not user:
            return await message.answer("Ваш профиль не найден. Введите команду /start.")
            
        # Запрашиваем из базы количество транзакций юзера
        tx_res = await db.execute(select(Transaction).where(Transaction.user_id == user.id))
        tx_count = len(tx_res.scalars().all())

    text = (
        f"👤 <b>Ваш Профиль</b>\n\n"
        f"💳 <b>ID:</b> <code>{user.telegram_id}</code>\n"
        f"👑 <b>Роль:</b> {'Администратор' if user.is_admin else 'Покупатель'}\n"
        f"💵 <b>Счёт:</b> ${user.balance}\n"
        f"🧾 <b>Личных транзакций (Escrow):</b> {tx_count}\n\n"
        f"<i>Все ваши сделки застрахованы умным Escrow-контрактом. Никто не имеет доступа к вашим средствам.</i> 🔒"
    )
    await message.answer(text, parse_mode="HTML")

@user_router.message(F.text == "ℹ️ Помощь")
async def process_help_button(message: Message):
    await message.answer("ℹ️ <b>Поддержка 24/7</b>\nНаш маркетплейс использует технологию безопасных P2P-сделок (Escrow). Свяжитесь с администрацией.", parse_mode="HTML")
