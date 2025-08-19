# Используем официальный образ Python 3.13 (slim — легковесный)
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
# --no-cache-dir — чтобы не засорять образ
# --upgrade — на всякий случай обновим pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . .

# Создаём папку для базы (на случай, если её нет)
RUN mkdir -p db

# Открываем порт 8000
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]