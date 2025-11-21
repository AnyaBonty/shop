# 1. Базовый образ Python
FROM python:3.12-slim

# 2. Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Устанавливаем Poetry
ENV POETRY_VERSION=2.2.1
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# 4. Не создавать виртуальное окружение внутри контейнера
ENV POETRY_VIRTUALENVS_CREATE=false

# 5. Рабочая директория
WORKDIR /app
ENV PYTHONPATH=/app

# 6. Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# 7. Устанавливаем только зависимости, без установки самого проекта
RUN poetry install --no-root --no-interaction --no-ansi

# 8. Копируем весь проект в контейнер
COPY . .

# 9. Указываем команду запуска: миграции Alembic + запуск FastAPI
CMD ["bash", "-c", "poetry run alembic upgrade head && poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"]
