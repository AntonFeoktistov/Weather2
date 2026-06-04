import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone

from weather.dtos import LocationDto, WeatherDto
from weather.models import Location
from weather.weather_finder import WeatherFinder

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
def test_location(test_user):
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


@pytest.fixture
def mock_finder(mocker):
    location_dto = LocationDto(name_en="London", name_ru="Лондон", lat=51.5, lon=-0.1)
    weather_dto = WeatherDto(
        location=location_dto, temperature=15.5, description="cloudy", wind_speed=5.2
    )
    mock_weather = weather_dto

    mock_finder = mocker.patch(
        "weather.views.refresh_weather_view.RefreshWeatherView.weather_finder"
    )
    mock_finder.get_weather_by_location_name.return_value = mock_weather

    return mock_finder


@pytest.fixture
def weather_finder():
    return WeatherFinder()


@pytest.fixture
def location_dto():
    return LocationDto(name_en="London", name_ru="Лондон", lat=51.5074, lon=-0.1278)
