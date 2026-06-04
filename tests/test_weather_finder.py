from unittest.mock import Mock, patch

import pytest
import requests

from weather.errors import LocationNotFoundError, WeatherNotFoundError

pytestmark = pytest.mark.django_db


def test_get_location_by_name_success(weather_finder):

    mock_response_data = [
        {
            "name": "London",
            "local_names": {"ru": "Лондон"},
            "lat": 51.5074,
            "lon": -0.1278,
            "country": "GB",
            "state": "England",
        }
    ]

    with patch("weather.weather_finder.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        result = weather_finder._get_location_by_name("London")

    assert result.name_en == "London"
    assert result.name_ru == "Лондон"
    assert result.lat == 51.507
    assert result.lon == -0.128


def test_get_location_not_found_raises_error(weather_finder):

    with patch("weather.weather_finder.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        with pytest.raises(LocationNotFoundError):
            weather_finder._get_location_by_name("fsiufhsuoehf_stuff_request")


def test_get_weather_by_location_success(weather_finder, location_dto):

    mock_response_data = {
        "cod": 200,
        "main": {"temp": 15.5},
        "weather": [{"description": "облачно"}],
        "wind": {"speed": 5.2},
    }

    with patch("weather.weather_finder.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        result = weather_finder._get_weather_by_location(location_dto)

    assert result.location.name_en == "London"
    assert result.temperature == 15.5
    assert result.description == "облачно"
    assert result.wind_speed == 5.2


def test_get_weather_api_error_raises_exception(weather_finder, location_dto):

    mock_response_data = {"cod": 401, "message": "Invalid API key"}

    with patch("weather.weather_finder.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        with pytest.raises(WeatherNotFoundError):
            weather_finder._get_weather_by_location(location_dto)


def test_get_location_timeout_raises_error(weather_finder):

    with patch("weather.weather_finder.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(LocationNotFoundError):
            weather_finder._get_location_by_name("London")
