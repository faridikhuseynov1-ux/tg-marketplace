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

# === СЕНЬОР-ФИЧА: ОБРАБОТКА DEEP-LINKING РЕФЕРАЛОВ ===
@user_router.message(CommandStart())
async def cmd_start(message: Message):
    args = message.text.split(" ")
    referrer_id = None
    
    # Парсим ссылку вида t.me/bot?start=ref_12345
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            referrer_id = int(args[1].split("_")[1])
            if referrer_id == message.from_user.id:
                referrer_id = None # Нельзя пригласить самого себя
        except ValueError:
            pass

    async with AsyncSessionLocal() as db:
        res = await db.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = res.scalars().first()
        
        if not user:
            # Создаем нового пользователя с указанием того, кто его пригласил
            new_user = User(
                telegram_id=message.from_user.id, 
                username=message.from_user.username, 
                balance=100.00,
                referred_by=referrer_id
            )
            db.add(new_user)
            await db.commit()
            
            # Начисляем бонус приглашающему (Реферальная программа!)
            if referrer_id:
                ref_res = await db.execute(select(User).where(User.telegram_id == referrer_id))
                referrer = ref_res.scalars().first()
                if referrer:
                    referrer.balance = float(referrer.balance) + 5.00
                    await db.commit()
                    
                    # Отправляем уведомление приглашающему при возможности (опускаем для упрощения)
            
            await message.answer(
                f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
                f"🎉 В честь регистрации мы начислили вам <b>$100.00</b>!\n"
                f"{('🎁 Вы приглашены пользователем! ' if referrer_id else '')}"
                f"Откройте [📱 Магазин] и совершите безопасную покупку.",
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
    web_app_url = os.getenv("WEB_APP_URL", "https://t.me/duров")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Открыть маркетплейс", web_app=WebAppInfo(url=web_app_url))]
    ])
    await message.answer("Каталог с оплатой Telegram Stars: ⭐️🛒", reply_markup=markup)

@user_router.message(F.text == "💰 Баланс")
async def process_balance_button(message: Message):
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = res.scalars().first()
        balance = user.balance if user else 0.00
    
    await message.answer(f"💰 Доступно: <b>${balance}</b>", parse_mode="HTML")

# === УЛУЧШЕНИЕ: ВЫВОД РЕФЕРАЛЬНОЙ ССЫЛКИ В ПРОФИЛЕ ===
@user_router.message(F.text == "👤 Профиль")
async def process_profile_button(message: Message):
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = res.scalars().first()
        if not user:
            return await message.answer("Профиль не найден. Введите /start.")
            
        tx_res = await db.execute(select(Transaction).where(Transaction.user_id == user.id))
        tx_count = len(tx_res.scalars().all())
        
        # Подсчет приглашенных друзей
        ref_res = await db.execute(select(User).where(User.referred_by == user.telegram_id))
        ref_count = len(ref_res.scalars().all())

    bot_info = await message.bot.me()
    ref_link = f"https://t.me/{bot_info.username}?start=ref_{user.telegram_id}"

    text = (
        f"👤 <b>Ваш Профиль</b>\n\n"
        f"💳 <b>ID:</b> <code>{user.telegram_id}</code>\n"
        f"👑 <b>Роль:</b> {'Администратор' if user.is_admin else 'Пользователь'}\n"
        f"💵 <b>Счёт:</b> ${user.balance}\n"
        f"🧾 <b>Транзакций (Escrow):</b> {tx_count}\n"
        f"👥 <b>Приглашено друзей:</b> {ref_count}\n\n"
        f"🔗 <b>Твоя реф. ссылка ($5 за друга!):</b>\n"
        f"<code>{ref_link}</code>\n\n"
        f"<i>Все ваши сделки застрахованы умным Escrow-контрактом.</i> 🔒"
    )
    await message.answer(text, parse_mode="HTML")

@user_router.message(F.text == "ℹ️ Помощь")
async def process_help_button(message: Message):
    await message.answer("ℹ️ <b>Поддержка 24/7</b>\nНаш маркетплейс использует Escrow-сделки. Зовите друзей и получайте доллары по реферальной программе!", parse_mode="HTML")
