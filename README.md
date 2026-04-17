# 🚀 P2P Telegram Marketplace (v4.0 The Senior Revolution)

## 🏢 Архитектура
Проект использует передовой Full-Stack:
- **База данных:** PostgreSQL 15, SQLAlchemy, Asyncpg
- **Бэкенд REST API:** FastAPI, JWT Authentication, Pydantic
- **Телеграм Бот:** aiogram 3.x, FSM (Finite State Machines)
- **Фронтенд:** React 18, Vite, TailwindCSS, Framer Motion, `@twa-dev/sdk`

## 🌟 Ключевые Фичи (Senior Level)

1. **Реферальная Система (Deep-Linking):**
   - Умный бот-маршрутизатор: поддержка ссылок `/start ref_<id>`.
   - Автоматическое начисление бонусов рефоводу прямо в бэкенде (+ $5.00).

2. **Full JWT Authentication Layer:**
   - Отказ от небезопасного проброса сырых Telegram `initData` в каждом запросе.
   - Эндпоинт `/api/v1/auth` проверяет подпись `HMAC-SHA256` и выдает криптографически стойкий **PyJWT Access Token**. 
   - React-приложение работает с защищенными маршрутами через `Authorization: Bearer <token>`.

3. **Safe Deal (Escrow механизм) и Webhook уведомления:**
   - При оформлении заказа в React Mini App, FastAPI проверяет баланс.
   - Сумма замораживается (`ItemStatus.PENDING`), создается транзакционный лог `ESCROW_HOLD`.
   - И самое главное: **FastAPI использует ядро Aiogram для отправки мгновенных Push-уведомлений (DMs) в Telegram покупателю и продавцу в режиме реального времени!** Никакого поллинга.

4. **Меню создания товаров через FSM:**
   - Панель CEO `/admin` содержит встроенный Конечный Автомат (FSM) для моментального добавления товаров прямо в чате бота, с мгновенным обновлением на React Ветрине.

5. **DevOps & Docker Orchestration:**
   - Готов к Deploy в 1 клик!
   - Команда: `docker-compose up --build -d` запускает СУБД, Сервер и Бота в изолированных контейнерах, автоматически пробрасывая порты и volume для PostgreSQL.

---
*Проект разработан и поддерживается автоматизированной архитектурой "Antigravity"*
