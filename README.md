# TestTaskPy - FastAPI приложение для управления задачами
## Описание
Простое REST API приложение для управления задачами, построенное на FastAPI с использованием TinyDB для хранения данных.

Предварительные требования
- Docker и Docker Compose
- Git (для клонирования репозитория)

## Установка и запуск
### 1. Клонирование репозитория
```bash
git clone <url-вашего-репозитория>
cd TestTaskPy
```
### 2. Установка Docker (если не установлен)
Для Debian:

```bash
sudo apt update
sudo apt install docker.io docker-compose
```
### 3. Запуск приложения
```bash
# Сборка и запуск в фоновом режиме
docker-compose up -d --build

# Или запуск в интерактивном режиме
docker-compose up --build
```
### 4. Проверка работы
Приложение будет доступно по адресу: http://localhost:8000

## Доступные endpoints:

GET /docs - Swagger документация

GET /tasks - Получить все задачи

GET /tasks/{id} - Получить задачу по ID

POST /tasks - Создать новую задачу

PUT /tasks/{id} - Обновить задачу

DELETE /tasks/{id} - Удалить задачу
