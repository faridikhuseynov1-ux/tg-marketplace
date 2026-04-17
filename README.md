# 🛒 Telegram P2P Marketplace (TMA)

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-Production_Ready-success.svg)
![NestJS](https://img.shields.io/badge/NestJS-E0234E?style=flat&logo=nestjs&logoColor=white)
![Prisma](https://img.shields.io/badge/Prisma-2D3748?style=flat&logo=prisma&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)
![Framer Motion](https://img.shields.io/badge/Framer_Motion-0055FF?style=flat&logo=framer&logoColor=white)

Это мощный P2P-маркетплейс, интегрированный прямо в Telegram с использованием технологии **Telegram Web Apps (TMA)**. Платформа позволяет пользователям выступать в роли продавцов и покупателей, имеет систему внутреннего баланса и поддерживает проведение безопасных сделок (Escrow).

---

## 🤖 Интеграция Телеграм и WebApp SDK

Проект представляет собой бесшовную экосистему из инлайн-бота и Web App:

- **Команда `/start`:** Бот приветствует пользователя по имени и выдаёт как Inline-кнопку, так и классическую Keyboard-кнопку для входа в Mini App.
- **Инлайн Покупки:** Введено меню каталога, позволяющее интуитивно совершать сделки прямо внутри мессенджера через Callback-кнопки (без открытия Mini App).
- **Связь Frontend -> Backend `WebApp.sendData`:** При оформлении заказа в корзине, WebView-приложение динамически получает ник и инфу о юзере через `initDataUnsafe`. При клике «Подтвердить покупку» WebApp автоматически сворачивается и отправляет payload с данными заказа боту через нативный `sendData`. В свою очередь, NestJS бэкенд мгновенно перехватывает этот `web_app_data` Event и самостоятельно инициирует транзакцию Escrow, завершая цепочку!

---

## 🏗 Архитектура

Архитектура платформы построена на принципах микромодульности и разделения ответственностей в рамках монорепы:

1. **Telegram Bot API & Backend (NestJS)**
   - Базируется в подпапке `backend/`. Обрабатывает REST запросы от Web App и управляет Telegram-ботом.
   - Внедрены строгие `DTO` с `class-validator`. Реализован кастомный `BigIntInterceptor` для безопасной конвертации PostgreSQL `BigInt`.

2. **База данных (PostgreSQL + Prisma)**
   - Модели: `User`, `Item`, `Category`, `Transaction`, `EscrowDeal`.
   - Использование типа `Decimal` для финансовой точности транзакций.

3. **Фронтенд - Mini App (React + Vite)**
   - Базируется в подпапке `frontend/`. 
   - Навигация и карточки товаров анимированы через **Framer Motion**.
   - UI автоматически адаптируется под темную или светлую тему Telegram.

---

## 🚀 Руководство по запуску

### 1. Подготовка Базы Данных (Prisma)
1. Создайте в корне `.env` с ключом `DATABASE_URL`.
2. Выполните генерацию схемы:
```bash
npm install
npx prisma db push
npx prisma generate
```

### 2. Запуск Backend
Создайте `.env` в папке `/backend` и добавьте `TELEGRAM_BOT_TOKEN`.
```bash
cd backend
npm install
npm run start:dev
```

### 3. Запуск Frontend
```bash
cd frontend
npm install
npm run dev
```

---
## 🛡 Безопасность
Проект успешно прошел аудит QA-команды. Реализованы глобальные пайпы валидации `ValidationPipe`, убран хардкод секретов, а БД защищена от коллизий сериализации.
