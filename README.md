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

## 🏗 Архитектура

Архитектура платформы (спроектирована @aydin) построена на принципах микромодульности и разделения ответственностей в рамках монорепы:

1. **Telegram Bot API & Backend (NestJS)**
   - Базируется в подпапке `backend/`. Обрабатывает REST запросы от Web App и управляет Telegram-ботом через `telegraf`.
   - Внедрены строгие `DTO` с `class-validator`. Реализован кастомный `BigIntInterceptor` для безопасной конвертации PostgreSQL `BigInt` (Telegram ID) в JSON string.
   - Управление конфигурацией производится через `@nestjs/config`.

2. **База данных (PostgreSQL + Prisma)**
   - Централизованная БД со сложными моделями: `User`, `Item`, `Category`, `Transaction` и `EscrowDeal`.
   - Жёсткие реляционные связи и использование типа `Decimal` для финансовой точности транзакций.

3. **Фронтенд - Mini App (React + Vite)**
   - Динамичный и сочный интерфейс (базируется в `frontend/`).
   - Навигация и карточки товаров анимированы через **Framer Motion**.
   - UI автоматически адаптируется под темную или светлую тему Telegram с помощью нативных CSS переменных интеграции `@twa-dev/sdk`.

---

## 🚀 Руководство по запуску

Следуйте простым шагам ниже, чтобы развернуть проект локально в режиме разработки.

### 1. Предварительные требования
- Node.js (v18+)
- PostgreSQL сервер (локально или в Docker)

### 2. Подготовка Базы Данных (Prisma)
В корневой папке проекта настройте окружение и поднимите БД:
```bash
# 1. Создайте в корне проекта файл .env 
# Впишите туда: DATABASE_URL="postgresql://user:password@localhost:5432/marketplace_db?schema=public"

# 2. Установите root-зависимости (для Prisma CLI)
npm install

# 3. Примените схему к БД и сгенерируйте Prisma Client
npx prisma db push
npx prisma generate
```

### 3. Запуск Backend (NestJS)
Перейдите в папку бэкенда и запустите сервер:
```bash
cd backend

# 1. Создайте .env в папке backend 
# TELEGRAM_BOT_TOKEN="Ваш_Токен_Бота"
# WEB_APP_URL="URL_Вашего_Web_App"

# 2. Установите зависимости
npm install

# 3. Запустите сервер (http://localhost:3000)
npm run start:dev
```

### 4. Запуск Frontend (React Web App)
В новом окне терминала перейдите в папку фронтенда:
```bash
cd frontend

# 1. Установите зависимости
npm install

# 2. Запустите dev-сервер (обычно http://localhost:5173)
npm run dev
```

---

## 🛡 Безопасность
Проект успешно прошел аудит QA-команды (@kamran). Реализованы глобальные пайпы валидации `ValidationPipe`, убран весь хардкод секретов, а БД защищена от коллизий сериализации кастомными NestJS Interceptors.
