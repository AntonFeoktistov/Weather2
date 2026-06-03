import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client
from django.utils import timezone
from myapp.models import Location

User = get_user_model()


@pytest.fixture
def client():
    return Client()


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
def test_weather_dict():
    return {
        "name": "London",
        "lat": "51.5074",
        "lon": "-0.1278",
        "temperature": "15.5",
        "description": "cloudy",
        "wind_speed": "5.2",
    }


@pytest.fixture
def test_location(db, test_user):
    location = Location.objects.create(
        user=test_user,
        name="London",
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


@pytest.fixture(autouse=True)
def clear_db():
    yield
    call_command("flush", verbosity=0, interactive=False)
