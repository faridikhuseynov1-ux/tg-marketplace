import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.future import select
from python_backend.db.database import AsyncSessionLocal
from python_backend.db.models import User, Item, ItemStatus

admin_router = Router()

CEO_ID_STR = os.getenv("CEO_TELEGRAM_ID", "123456789")
CEO_ID = int(CEO_ID_STR) if CEO_ID_STR.isdigit() else 0

admin_router.filter(F.from_user.id == CEO_ID)

# === СЕНЬОР-ФИЧА: FSM (Конечный Автомат) для добавления товаров ===
class AddItemState(StatesGroup):
    waiting_for_title = State()
    waiting_for_price = State()

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="➕ Добавить Товар", callback_data="admin_add_item")],
        [InlineKeyboardButton(text="📨 Рассылка", callback_data="admin_broadcast")]
    ])
    await message.answer("🛠 <b>Секретная Панель Управления CEO</b>", reply_markup=markup)

@admin_router.callback_query(F.data == "admin_stats")
async def process_admin_stats(callback: CallbackQuery):
    await callback.answer()
    async with AsyncSessionLocal() as db:
        user_count = len((await db.execute(select(User))).scalars().all())
        item_count = len((await db.execute(select(Item))).scalars().all())
        
    await callback.message.answer(
        f"📊 <b>Живая Статистика из БД:</b>\n\n"
        f"👥 Зарегистрировано: {user_count} юзеров\n"
        f"📦 Размещено товаров: {item_count}"
    )

# --- Начинаем процесс добавления товара ---
@admin_router.callback_query(F.data == "admin_add_item")
async def process_add_item_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("📝 Введите НАЗВАНИЕ нового товара (например: 'Spotify Premium'):")
    await state.set_state(AddItemState.waiting_for_title)

@admin_router.message(AddItemState.waiting_for_title)
async def process_add_item_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("💰 Отлично. Теперь введите ЦЕНУ в долларах (например: 15.50):")
    await state.set_state(AddItemState.waiting_for_price)

@admin_router.message(AddItemState.waiting_for_price)
async def process_add_item_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        return await message.answer("❌ Ошибка! Введите число, например: 15.50")
    
    data = await state.get_data()
    title = data['title']
    
    async with AsyncSessionLocal() as db:
        # Узнаем ID админа в БД
        res = await db.execute(select(User).where(User.telegram_id == message.from_user.id))
        admin_user = res.scalars().first()
        
        new_item = Item(seller_id=admin_user.id, title=title, price=price, status=ItemStatus.ACTIVE)
        db.add(new_item)
        await db.commit()
        
    await message.answer(f"✅ База данных обновлена!\nТовар <b>{title}</b> за <b>${price:.2f}</b> успешно добавлен в маркетплейс!\nЗапускай Mini App, он уже там!", parse_mode="HTML")
    await state.clear()
