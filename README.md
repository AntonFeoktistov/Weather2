# Weather2

Веб-приложение на Django: регистрация и вход, поиск погоды через OpenWeather API, сохранение избранных локаций с обновлением данных.

**Стек:** Django 6, PostgreSQL, Pydantic, pytest, Docker / Docker Compose.

## Возможности

- Регистрация с кастомной валидацией пароля
- Поиск погоды по названию города
- Список избранных локаций (добавление, удаление, массовое обновление погоды)
- Интеграция с [OpenWeather](https://openweathermap.org/api)

## Структура проекта

```
core/           # настройки Django, urls
users/          # регистрация, login/logout
weather/        # локации, OpenWeather, views
templates/      # HTML-шаблоны
tests/          # pytest (интеграционные и unit)
```

## Требования

- Docker и Docker Compose **или**
- Python 3.12+, PostgreSQL 16

## Переменные окружения

Создайте файл `.env` в корне проекта (не коммитьте в git). Пример:

```env
# Django
SECRET_KEY=длинная-случайная-строка
DEBUG=True

# PostgreSQL (имена должны совпадать с docker-compose или вашей БД)
POSTGRES_DB=myproject
POSTGRES_USER=myproject
POSTGRES_PASSWORD=смените-на-сильный-пароль
POSTGRES_HOST=db
POSTGRES_PORT=5432

# OpenWeather — ключ: https://openweathermap.org/api
OPENWEATHER_API_KEY=ваш-ключ
OPENWEATHER_LOCATION_URL=http://api.openweathermap.org/geo/1.0/direct
OPENWEATHER_WEATHER_URL=https://api.openweathermap.org/data/2.5/weather
```

> **Важно:** `settings.py` читает `POSTGRES_*`, а не `DATABASE_URL`. В `docker-compose.yml` для сервиса `web` нужно передать те же переменные (см. раздел про деплой).

Для production дополнительно (после доработки `settings.py`):

```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

## Локальный запуск (Docker)

```bash
git clone <repo-url>
cd Weather2
cp .env.example .env   # или создайте .env вручную по образцу выше
# заполните SECRET_KEY и OPENWEATHER_API_KEY

docker compose up --build
```

Приложение: http://localhost:8000  
Админка: http://localhost:8000/admin/ (нужен `createsuperuser`).

### Миграции и суперпользователь

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

### Тесты

```bash
docker compose --profile tests run --rm tests
```

Или локально (нужен PostgreSQL и `.env`):

```bash
pip install -r requirements.txt
pytest
```

## Локальный запуск без Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# PostgreSQL должен быть доступен; в .env: POSTGRES_HOST=localhost

python manage.py migrate
python manage.py runserver
```

---

## Перед деплоем на VPS (чеклист)

Текущий `docker-compose.yml` и `settings.py` рассчитаны на **разработку**. Перед выкладкой на удалённый сервер пройдите этот список.

### 1. Безопасность Django

| Шаг | Действие |
|-----|----------|
| ☐ | Сгенерировать новый `SECRET_KEY` (не использовать dev-ключ): `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| ☐ | `DEBUG=False` в `.env` на сервере |
| ☐ | Задать `ALLOWED_HOSTS` — IP VPS и/или домен |
| ☐ | Задать `CSRF_TRUSTED_ORIGINS` с `https://` для домена |
| ☐ | Включить `AUTH_PASSWORD_VALIDATORS` в `settings.py` (сейчас список пустой) |
| ☐ | Запустить `python manage.py check --deploy` в production-окружении |

### 2. Секреты и `.env`

| Шаг | Действие |
|-----|----------|
| ☐ | Уникальные пароли `POSTGRES_PASSWORD`, `SECRET_KEY` только на VPS |
| ☐ | Файл `.env` только на сервере, права `chmod 600` |
| ☐ | Не публиковать порт PostgreSQL (`5432`) наружу — БД только внутри Docker-сети |
| ☐ | Проверить, что `.env` в `.gitignore` и не попал в репозиторий |

### 3. Docker под production

| Шаг | Действие |
|-----|----------|
| ☐ | Убрать монтирование `.:/app` у `web` — код должен быть в образе (`COPY` в Dockerfile) |
| ☐ | Заменить `runserver` на **Gunicorn** (или uWSGI), например: `gunicorn core.wsgi:application --bind 0.0.0.0:8000` |
| ☐ | Добавить в `requirements.txt`: `gunicorn` |
| ☐ | Пробросить в `web` все переменные из `.env` (`env_file: .env` или `environment:`) |
| ☐ | Согласовать имена БД: `POSTGRES_*` в compose и в `settings.py` (сейчас в compose есть `DATABASE_URL`, но Django его не использует) |
| ☐ | `collectstatic` при сборке/старте, если появятся CSS/JS; настроить `STATIC_ROOT` |
| ☐ | Отдельный `docker-compose.prod.yml` (рекомендуется), не трогать dev-compose |

### 4. Домен и HTTPS

| Шаг | Действие |
|-----|----------|
| ☐ | DNS A-запись на IP VPS |
| ☐ | Reverse proxy (Nginx / Caddy / Traefik) перед контейнером `web` |
| ☐ | TLS-сертификат (Let's Encrypt) |
| ☐ | Проксировать на `127.0.0.1:8000` или внутренний порт compose, не светить Gunicorn в интернет напрямую |

### 5. Данные и обслуживание

| Шаг | Действие |
|-----|----------|
| ☐ | Volume `postgres_data` для сохранения БД при перезапуске |
| ☐ | План бэкапов PostgreSQL (`pg_dump` по cron) |
| ☐ | Логи: `docker compose logs -f web`, ротация на хосте |
| ☐ | Ограничить SSH (ключи, отключить root-login), firewall (ufw): 22, 80, 443 |

### 6. OpenWeather

| Шаг | Действие |
|-----|----------|
| ☐ | Production API key с лимитами, привязанный к проекту |
| ☐ | Убедиться, что VPS имеет исходящий HTTPS к `api.openweathermap.org` |

### 7. Финальная проверка

```bash
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate
docker compose -f docker-compose.prod.yml run --rm web python manage.py check --deploy
docker compose -f docker-compose.prod.yml up -d
```

---

## Деплой на VPS (Docker)

Ниже — типовой сценарий после выполнения чеклиста выше.

### На VPS (Ubuntu/Debian)

**1. Установить Docker**

```bash
sudo apt update
sudo apt install -y ca-certificates curl
# установка Docker по официальной документации: https://docs.docker.com/engine/install/
sudo usermod -aG docker $USER
# перелогиниться
```

**2. Клонировать проект**

```bash
git clone <repo-url> /opt/weather2
cd /opt/weather2
```

**3. Создать `.env` на сервере**

```bash
nano .env
chmod 600 .env
```

Заполнить production-значения (см. таблицу переменных). `POSTGRES_HOST=db` для Compose.

**4. Production Compose (пример идеи)**

Создайте `docker-compose.prod.yml` без публикации Postgres и с Gunicorn:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  web:
    build: .
    env_file: .env
    command: gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "127.0.0.1:8000:8000"
    restart: unless-stopped

volumes:
  postgres_data:
```

**5. Собрать и запустить**

```bash
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

**6. Nginx (кратко)**

На хосте установить Nginx, проксировать `your-domain.com` → `http://127.0.0.1:8000`, выдать сертификат (certbot). В Django — `CSRF_TRUSTED_ORIGINS` и `SECURE_PROXY_SSL_HEADER` при работе за proxy.

**7. Обновление версии**

```bash
cd /opt/weather2
git pull
docker compose -f docker-compose.prod.yml build web
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

---

## Маршруты приложения

| URL | Описание |
|-----|----------|
| `/` | Главная (гости) |
| `/register/` | Регистрация |
| `/login/` | Вход |
| `/home/` | Погода и избранные локации (требуется вход) |
| `/admin/` | Админка Django |

## Разработка

- Тесты: `pytest` (каталог `tests/`)
- Часовой пояс: `Europe/Minsk`
- Внешний API: геокодинг + current weather OpenWeather

## Лицензия

Уточните лицензию для репозитория при публикации.
