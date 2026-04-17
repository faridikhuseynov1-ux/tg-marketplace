import os
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

user_router = Router()

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Генерация базовой Reply-клавиатуры для пользователя"""
    kb = [
        [KeyboardButton(text="📱 Магазин"), KeyboardButton(text="💰 Баланс")],
        [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="ℹ️ Помощь")]
    ]
    # resize_keyboard=True делает клавиатуру компактной
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    """Штатная команда /start - Выводим приветствие и Reply-меню"""
    user_name = message.from_user.first_name or "Пользователь"
    text = (
        f"👋 Привет, <b>{user_name}</b>!\n\n"
        f"Добро пожаловать в <b>TG-Marketplace</b>.\n"
        f"Выбери нужный раздел в нижнем меню 👇"
    )
    await message.answer(text, reply_markup=get_main_keyboard())

@user_router.message(F.text == "📱 Магазин")
async def process_shop_button(message: Message):
    """Обработка кнопки 'Магазин' из Reply-меню"""
    # URL нашего Mini App Frontend
    web_app_url = os.getenv("WEB_APP_URL", "https://t.me/durov")
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Открыть маркетплейс", web_app=WebAppInfo(url=web_app_url))]
    ])
    
    await message.answer(
        "Нажми на кнопку ниже, чтобы открыть наш супер-современный Mini App магазин! 🛒",
        reply_markup=markup
    )

@user_router.message(F.text == "💰 Баланс")
async def process_balance_button(message: Message):
    # Заглушка, в будущем сюда подключится вызов в SQLAlchemy для получения юзера
    await message.answer("Ваш текущий баланс: <b>$0.00</b>\n(Скоро будет интеграция с БД)", parse_mode="HTML")

@user_router.message(F.text == "👤 Профиль")
async def process_profile_button(message: Message):
    await message.answer("👤 <b>Ваш Профиль</b>\nБлок статистики и истории сделок находится в разработке.", parse_mode="HTML")

@user_router.message(F.text == "ℹ️ Помощь")
async def process_help_button(message: Message):
    await message.answer("ℹ️ <b>Помощь:</b>\nНаш маркетплейс использует технологию безопасных P2P-сделок (Escrow). Если у вас возникли проблемы, обратитесь в поддержку.", parse_mode="HTML")
