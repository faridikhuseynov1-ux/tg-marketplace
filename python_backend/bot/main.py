import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from python_backend.bot.handlers.user import user_router
from python_backend.bot.handlers.admin import admin_router

logging.basicConfig(level=logging.INFO)

async def main():
    # Токен бота извлекаем из окружения
    token = os.getenv("TELEGRAM_BOT_TOKEN", "12345:DUMMY_TOKEN")
    if token == "12345:DUMMY_TOKEN":
        logging.warning("Внимание! Используется фейковый токен. Пожалуйста укажите TELEGRAM_BOT_TOKEN в .env!")
    
    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher()

    # Сначала подключаем админский роутер, потом пользовательский
    dp.include_router(admin_router) 
    dp.include_router(user_router)

    logging.info("Бот на базе aiogram 3.x успешно запущен. Начинаем Long Polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
