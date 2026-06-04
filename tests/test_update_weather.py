import pytest
from django.contrib.auth import get_user_model

from tests.urls import urls
from weather.errors import WeatherNotFoundError

pytestmark = pytest.mark.django_db


User = get_user_model()
pytestmark = pytest.mark.django_db


def test_refresh_updates_weather(auth_client, test_location, mock_finder):
    old_updated_at = test_location.weather_updated_at

    response = auth_client.post(urls.refresh_url, HTTP_REFERER=urls.home_url)

    assert response.status_code == 302

    test_location.refresh_from_db()
    assert old_updated_at != test_location.weather_updated_at

    mock_finder.get_weather_by_location_name.assert_called_once_with(test_location.name)


def test_refresh_handles_weather_not_found(auth_client, test_location, mock_finder):

    mock_finder.get_weather_by_location_name.side_effect = WeatherNotFoundError()

    response = auth_client.post(urls.refresh_url, HTTP_REFERER=urls.home_url)

    assert response.status_code == 302
    mock_finder.get_weather_by_location_name.assert_called_once()
