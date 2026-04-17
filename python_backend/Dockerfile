FROM python:3.11-slim

WORKDIR /app

# Обновляем pip и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходники бэкенда
COPY . .

# Устанавливаем PYTHONPATH, чтобы модули находили друг друга (from python_backend.X)
ENV PYTHONPATH=/app/..
