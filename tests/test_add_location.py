import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from tests.urls import urls
from weather.models import Location

User = get_user_model()
pytestmark = pytest.mark.django_db


def test_unauthenticated_user_cannot_add_location(client, test_weather_dict):
    count_before = Location.objects.filter(name=test_weather_dict["name"]).count()
    response = client.post(urls.add_location_url, test_weather_dict)
    count_after = Location.objects.filter(name=test_weather_dict["name"]).count()
    assert response.status_code == 302
    assert count_before == count_after


def test_successful_location_addition(auth_client, test_user, test_weather_dict):
    response = auth_client.post(
        urls.add_location_url, test_weather_dict, HTTP_REFERER=urls.referer
    )

    assert response.status_code == 302
    assert response.url == urls.referer

    location = Location.objects.filter(
        user=test_user, name=test_weather_dict["name"]
    ).first()

    assert location is not None
    assert location.lat
    assert location.weather_data["temperature"] == float(
        test_weather_dict["temperature"]
    )
    assert location.weather_data["description"] == test_weather_dict["description"]
    assert location.weather_updated_at is not None

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0
    assert "добавлена" in str(messages[0])


def test_add_duplicate_location(
    auth_client, test_user, test_location, test_weather_dict
):
    auth_client.post(
        urls.add_location_url, test_weather_dict, HTTP_REFERER=urls.referer
    )
    auth_client.post(
        urls.add_location_url, test_weather_dict, HTTP_REFERER=urls.referer
    )
    assert (
        Location.objects.filter(user=test_user, name=test_weather_dict["name"]).count()
        == 1
    )
