import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

admin_router = Router()

# Вытягиваем ID CEO из переменной окружения
CEO_ID_STR = os.getenv("CEO_TELEGRAM_ID", "123456789")
CEO_ID = int(CEO_ID_STR) if CEO_ID_STR.isdigit() else 0

# ИСПРАВЛЕНИЕ QA (Kamran):
# Вешаем фильтр на ВЕСЬ роутер: сюда попадут ТОЛЬКО апдейты от CEO (и сообщения, и колбэки)
admin_router.filter(F.from_user.id == CEO_ID)

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Скрытая команда /admin, доступная только для CEO"""
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📨 Рассылка", callback_data="admin_broadcast")]
    ])
    
    await message.answer(
        "🛠 <b>Секретная Панель Управления CEO</b>\n\nВыберите действие:",
        reply_markup=markup
    )

@admin_router.callback_query(F.data == "admin_stats")
async def process_admin_stats(callback: CallbackQuery):
    await callback.answer()
    
    # В будущем тут будет SELECT count(*) из PostgreSQL/SQLAlchemy
    await callback.message.answer("📊 <b>Системная Статистика:</b>\n\nПользователей: 1450\nТранзакций (Escrow): 392\nОбщий оборот: $12,450.00")

@admin_router.callback_query(F.data == "admin_broadcast")
async def process_admin_broadcast(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("📨 Режим рассылки активирован. Отправьте сообщение, которое хотите разослать всем пользователям (в разработке).")
