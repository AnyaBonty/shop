# Shop API — интернет-магазин на FastAPI

Бэкенд интернет-магазина с JWT-авторизацией, ролями, корзиной и заказами.

В документации можно зайти в аккаунт с помощью формы, разлогинится и удалить аккаунты с помощью эндпоинтов.

## Стек
- Python 3.12
- FastAPI (async)
- SQLAlchemy 2.0 + Alembic
- PostgreSQL
- Redis (для хранения активных токенов)
- Poetry (управление зависимостями)
- Docker + docker-compose

## Роли пользователей
| Роль       | id | Описание                     | По умолчанию |
|------------|----|------------------------------|--------------|
| `user`     | 1  | Обычный зарегистрированный пользователь | Yes       |
| `customer` | 2  | Покупатель (для совместимости)       | —         |
| `manager`  | 3  | Менеджер магазина                         | —         |
| `admin`    | 4  | Полный доступ (суперпользователь)         | —         |

Суперпользователь создаётся автоматически при первом запуске:  
`admin@shop.ru` / `admin123` (сменить в `.env`)

## Быстрый старт

### Вариант 1 — через Docker (рекомендуется)
```bash
# Клонируем и заходим
git clone <твой-репозиторий>
cd shop

# Копируем .env
cp .env.example .env

# Запускаем всё одной командой
docker compose up --build

API доступен по адресу: http://localhost:8000
Документация (Swagger): http://localhost:8000/docs
```




### Вариант 2 — локально (для разработки)
Bash
```
# Устанавливаем зависимости
poetry install

# Копируем .env
cp .env.example .env

# Запускаем PostgreSQL и Redis через Docker
docker compose up postgres redis -d

# Применяем миграции
poetry run alembic upgrade head

# Запускаем сервер
poetry run uvicorn backend.app.main:app --reload
→ http://127.0.0.1:8000/docs
```


