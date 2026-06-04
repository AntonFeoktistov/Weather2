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

## Переменные окружения

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


## Локальный запуск (Docker)

```bash
git clone <repo-url>
cd Weather2
cp .env.example .env   # или создайте .env вручную по образцу выше
# заполните SECRET_KEY и OPENWEATHER_API_KEY

docker compose up --build
```

Приложение: http://localhost:8000  


### Миграции и суперпользователь

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

### Тесты

```bash
docker compose --profile tests run --rm tests
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

## Маршруты приложения

| URL | Описание |
|-----|----------|
| `/` | Главная (гости) |
| `/register/` | Регистрация |
| `/login/` | Вход |
Доступ только по логину:
| `/home/` | Погода и избранные локации (требуется вход) |
| `/home/add_location` | Добавление локации|
| `/home/delete_location` | Удаление локации |
| `/home/refresh_weather` | Обновление погоды в локациях пользователя |


