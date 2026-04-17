import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from python_backend.db.database import DATABASE_URL, Base
from python_backend.db.models import User, Item, ItemStatus

async def main():
    print("Подключаюсь к Базе Данных...")
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    # 1. Создаем все таблицы (а-ля Alembic, но проще для старта)
    async with engine.begin() as conn:
        print("Создаю таблицы...")
        await conn.run_sync(Base.metadata.create_all)
    
    # 2. Фабрика сессий
    session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)
    
    async with session_maker() as session:
        # 3. Проверка на наличие данных (чтобы не дублировать при повторном запуске)
        from sqlalchemy.future import select
        res = await session.execute(select(User).limit(1))
        if res.scalars().first():
            print("❌ База уже наполнена (Seed был запущен ранее). Отмена.")
            return
            
        print("Создаю первого системного администратора...")
        admin = User(
            telegram_id=111222333, # Fake ID
            username="system_seller", 
            balance=50000.00, 
            is_admin=True
        )
        session.add(admin)
        await session.commit()
        await session.refresh(admin) # Получаем его ID из базы
        
        print("Создаю тестовые товары (Они появятся в React-приложении!)...")
        items = [
            Item(seller_id=admin.id, title="Telegram Premium (1 Year)", price=29.99, status=ItemStatus.ACTIVE),
            Item(seller_id=admin.id, title="Python + React Pro Course", price=149.00, status=ItemStatus.ACTIVE),
            Item(seller_id=admin.id, title="Exclusive Monkey NFT", price=450.50, status=ItemStatus.ACTIVE),
            Item(seller_id=admin.id, title="VPN Server Configuration", price=15.00, status=ItemStatus.ACTIVE),
        ]
        
        session.add_all(items)
        await session.commit()
        print("✅ Успех! База данных наполнена реальными товарами. Фронтенд готов их получить!")

if __name__ == "__main__":
    asyncio.run(main())
