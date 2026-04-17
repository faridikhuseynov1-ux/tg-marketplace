# 🛒 Telegram P2P Marketplace (Python Stack)

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-Production_Ready-success.svg)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-2C3E50?style=flat)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Async-D71F00?style=flat)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)

P2P-маркетплейс нового поколения, встроенный в Telegram с помощью **Web Apps (TMA)**. 
Пилотный проект полностью переведен на сверхбыстрый и мощный асинхронный стек Python, гарантирующий максимальную производительность при работе с Telegram API.

---

## 🏗 Архитектура

Наш монорепозиторий состоит из двух неразрывных слоев:

1. **Python Бэкенд (`/python_backend`)**
   - **Бот (aiogram 3.x):** Аппарат лонг-поллинга, обрабатывающий все команды и коллбеки напрямую в мессенджере.
   - **REST API (FastAPI):** Скоростной сервер для безопасной обработки финансовых данных (`initData`) от React-фронтенда.
   - **База Данных (PostgreSQL + SQLAlchemy 2.0):** Асинхронные модели (`User`, `Item`, `Ad`, `Transaction`) с высокоточной арифметикой для балансов (`Numeric`).

2. **React Фронтенд (`/frontend`)**
   - Интерактивный WebApp интерфейс (Vite + React + Tailwind + Framer Motion).
   - Стучится напрямую в зашифрованные эндпоинты FastAPI с fallback'ами к нативным методам `WebApp.sendData()`.

---

## 🤖 Интерфейс Бота

В версии 2.0 бот использует навигационную **Reply-клавиатуру**, которая всегда закреплена внизу чата для интуитивного доступа:

*   `[📱 Магазин]` — Точка входа. При нажатии бот присылает сообщение-знакомство с WebApp-кнопкой (Inline), открывающей наш React Mini App.
*   `[💰 Баланс]` — Моментальный запрос текущего счета пользователя прямо в чате без загрузки WebView.
*   `[👤 Профиль]` — Статистика сделок юзера (куплено товаров/продано/рейтинг).
*   `[ℹ️ Помощь]` — Встроенный FAQ по Escrow-безопасности и контакт службы поддержки (Support).

*Скрытая Админ-панель:* Доступна только для CEO проекта по статичному Telegram-ID через команду `/admin`. Включает модули глобальной рассылки (Broadcast) и защищенной аналитики платформы.

---

## 🚀 Руководство по запуску

Для развертывания проекта локально следуйте этим простым шагам:

### Шаг 1: Настройка Python Backend

1. **Создайте и активируйте виртуальное окружение (venv)** внутри подпапки бэкенда:
   ```bash
   cd python_backend
   python -m venv venv
   
   # Способ активации на Windows:
   venv\Scripts\activate
   
   # Способ активации на MacOS/Linux:
   source venv/bin/activate
   ```

2. **Установите все Python зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте переменные окружения:**
   Внутри папки `python_backend` создайте файл `.env` и добавьте базовые ключи:
   ```env
   TELEGRAM_BOT_TOKEN="ВАШ_ТОКЕН_БОТА_ОТ_BOTFATHER"
   CEO_TELEGRAM_ID="ВАШ_TELEGRAM_ID"
   DATABASE_URL="postgresql+asyncpg://user:password@localhost/marketplace_db"
   WEB_APP_URL="https://ваша-ссылка-на-react"
   ```

4. **Запустите aiogram бота:**
   ```bash
   python main.py
   ```
   *P.S. (Инструкция по запуску Uvicorn/FastAPI-сервера будет в отдельном сервисном файле).*

### Шаг 2: Настройка Frontend (React TMA)

Для работы визуального интерфейса откройте второй терминал:
```bash
cd frontend
npm install
npm run dev
```

Всё готово! Бот мгновенно реагирует на команды в Telegram, а React отрисовывает роскошный P2P дизайн! 🚀

---
## 🛡 QA Аудит прошел успешно
Система проверена. Уязвимости инлайн-хэндлеров админки исправлены (глобальные фильтры `aiogram`). Валидация `WebApp.initData` через HMAC SHA-256 обеспечивает банковский уровень безопасности.
