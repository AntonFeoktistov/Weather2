import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client
from django.urls import reverse
from myapp.models import Location

from weather.dtos import LocationDto, WeatherDto

User = get_user_model()


@pytest.fixture
def register_url():
    return reverse("users:register")


@pytest.fixture
def login_url():
    return reverse("users:register")


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def test_user_data():
    return {"username": "testuser", "password": "testpass123"}


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser",
        password="testpass123",
    )


@pytest.fixture
def auth_client(client, test_user):
    client.login(username="testuser", password="testpass123")
    return client


@pytest.fixture
def test_weather_data():
    location_dto = LocationDto(name_en="London", name_ru="Лондон", lat=51.5, lon=-0.1)
    weather_dto = WeatherDto(
        location=location_dto, temperature=15.5, description="cloudy", wind_speed=5.2
    )
    return weather_dto


@pytest.fixture
def test_location(db, test_user):
    location = Location.objects.create(
        user=test_user,
        name_en="London",
        name_ru="Лондон",
        lat=51.5,
        lon=-0.1,
        weather_data={
            "temperature": 15.5,
            "description": "cloudy",
            "wind_speed": 5.2,
        },
        weather_updated_at=timezone.now(),
    )
    return location


# ============================================
# ПРОДВИНУТЫЕ ФИКСТУРЫ (для сложных сценариев)
# ============================================


@pytest.fixture
def multiple_locations(db, test_user):
    """Несколько локаций для одного пользователя"""
    locations = [
        Location.objects.create(
            user=test_user,
            name_en="London",
            name_ru="Лондон",
            lat=51.5,
            lon=-0.1,
            weather_data={
                "temperature": 15.5,
                "description": "cloudy",
                "wind_speed": 5.2,
            },
        ),
        Location.objects.create(
            user=test_user,
            name_en="Paris",
            name_ru="Париж",
            lat=48.8,
            lon=2.3,
            weather_data={
                "temperature": 20.0,
                "description": "sunny",
                "wind_speed": 3.0,
            },
        ),
    ]
    return locations


# ============================================
# ФИКСТУРЫ ДЛЯ API (аналог FastAPI client + auth_client)
# ============================================


@pytest.fixture
def api_client():
    """API клиент (для тестирования эндпоинтов, возвращающих JSON)"""
    from rest_framework.test import APIClient  # если используешь DRF

    return APIClient()


@pytest.fixture
def auth_api_client(api_client, test_user):
    """Авторизованный API клиент"""
    api_client.force_authenticate(user=test_user)  # для DRF
    return api_client


# ============================================
# ФИКСТУРЫ ДЛЯ ОЧИСТКИ БД
# ============================================


@pytest.fixture(autouse=True)
def clear_db():
    """Автоматически очищает таблицы после теста (опционально)"""
    yield
    call_command("flush", verbosity=0, interactive=False)


# ============================================
# ПРИМЕР ТЕСТА
# ============================================


@pytest.mark.django_db
def test_user_registration(client):
    """Тест регистрации пользователя"""
    response = client.post(
        "/register/",
        {
            "username": "newuser",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "email": "new@example.com",
        },
    )
    assert response.status_code == 302  # редирект после успешной регистрации
    assert User.objects.filter(username="newuser").exists()
