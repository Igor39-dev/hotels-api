# Система бронирования отелей

REST API для сервиса бронирования отелей. Позволяет управлять отелями, номерами,
удобствами и бронированиями, а также искать номера, свободные на заданный период.

## Ключевые технологии

### 1. Фреймворк FastAPI
- REST API на **FastAPI** с полностью асинхронной обработкой запросов (`async`/`await`).
- Автоматическая документация **Swagger UI** (`/docs`) и OpenAPI-схема.
- Внедрение зависимостей через **Depends**.

### 2. Работа с данными
- База данных — **PostgreSQL**.
- ORM — **SQLAlchemy** (2.0, async, драйвер `asyncpg`).
- Миграции схемы БД — **Alembic**.
- Валидация и сериализация данных — схемы **Pydantic** (`pydantic-settings` для конфигурации).
- Архитектурные паттерны: **DTO**, **Repository**, **Service**, **Data Mapper**.
- Аутентификация и авторизация — **JWT** (access-токены, хеширование паролей).

### 3. Инфраструктура приложения
- Кэширование — **Redis**.
- Фоновые задачи — **Celery** (worker + beat).
- Тестирование — **pytest** (изоляция БД через `NullPool`).
- Линтинг и форматирование — **ruff**.
- Логирование — стандартный `logging`.

### 4. Развёртывание
- Контейнеризация — **Docker**.
- Деплой — **Nginx** (reverse proxy на `booking_back:8001` с ограничением частоты запросов `1r/s` на IP).
- **CI/CD** — GitLab Runner (стадии `build`, `lint_format`, `migrations`, `test`, `deploy`).

## Архитектура и структура проекта

    src/
    ├── api/           # HTTP-роутеры FastAPI (auth, hotels, rooms, bookings, facilities, images)
    ├── connectors/    # подключения к внешним сервисам (Redis и др.)
    ├── models/        # ORM-модели SQLAlchemy
    ├── repositories/  # слой доступа к данным (паттерн Repository)
    │   └── mappers/   # преобразование ORM-моделей в доменные сущности (Data Mapper)
    ├── services/      # бизнес-логика (паттерн Service)
    ├── shemas/        # Pydantic-схемы (DTO)
    ├── migrations/    # миграции Alembic
    ├── tasks/         # фоновые задачи Celery
    ├── utlils/        # вспомогательные утилиты (в т.ч. DBManager)
    ├── config.py      # конфигурация приложения (pydantic-settings)
    ├── database.py    # инициализация подключения к БД
    ├── exceptions.py  # доменные исключения
    └── main.py        # точка входа приложения

    tests/             # тесты (pytest)

## Конфигурация

Настройки читаются из переменных окружения / файла `.env` (`src/config.py`):

- `MODE` — режим работы: `TEST`, `LOCAL`, `DEV`, `PROD`.
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME` — подключение к PostgreSQL.
- `REDIS_HOST`, `REDIS_PORT` — подключение к Redis.
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` — параметры JWT.

## Запуск

### Создание сети

    docker network create myNetwork

### Контейнер для БД

    docker run --name booking_db \
        -p 6432:5432 \
        -e POSTGRES_USER=abcde \
        -e POSTGRES_PASSWORD=abcdkqptyoiqnae \
        -e POSTGRES_DB=booking \
        --network=myNetwork \
        --volume pg-booking-data:/var/lib/postgresql/data \
        -d postgres:16

### Контейнер для Redis

    docker run --name booking_cache \
        -p 7379:6379 \
        --network=myNetwork \
        -d redis:7-alpine

### Сборка образа приложения

    docker build -t booking_image .

### Контейнер для приложения (Hotels-API)

    docker run --name booking-back \
        -p 7777:8001 \
        --network=myNetwork \
        booking_image

При старте контейнера автоматически применяются миграции и запускается приложение:

    alembic upgrade head && python src/main.py

### Контейнер для Celery worker

    docker run --name booking_celery_worker \
        --network=myNetwork \
        booking_image \
        celery --app=src.tasks.celery_app:celery_instance worker -l INFO

### Контейнер для Celery beat

    docker run --name booking_celery_beat \
        --network=myNetwork \
        booking_image \
        celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

### Контейнер для Nginx

    docker run --name booking_nginx \
        --volume ./nginx.conf:/etc/nginx/nginx.conf \
        --network=myNetwork \
        --rm -p 80:80 nginx

## Миграции

    alembic revision --autogenerate -m "add table"
    alembic upgrade head

## Тестирование

    pytest

## CI/CD (GitLab Runner)

Конвейер (`.gitlab-ci.yml`) состоит из стадий:

- `build` — копирование `.env` / `.env-test` из CI-переменных и сборка образа `booking-api-image`.
- `lint_format` — `ruff check` и `ruff format --check`.
- `migrations` — `alembic upgrade head`.
- `test` — `pytest -s -v`.
- `deploy` — `docker compose -f docker-compose-ci.yml up -d` и перезагрузка nginx.

### Контейнер для gitlab-runner

    docker run -d --name gitlab-runner --restart always \
        -v /srv/gitlab-runner/config:/etc/gitlab-runner \
        -v /var/run/docker.sock:/var/run/docker.sock \
        gitlab/gitlab-runner:latest

### Регистрация gitlab-runner

    docker run --rm -it -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner:latest register
