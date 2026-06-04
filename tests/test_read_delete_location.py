import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from tests.urls import urls
from weather.models import Location

User = get_user_model()
pytestmark = pytest.mark.django_db


def test_get_locations_unauthorized(client):
    response = client.get(urls.home_url)

    assert response.status_code == 302
    assert response.url.startswith("/login/")


def test_get_locations(auth_client, test_weather_dict):

    response = auth_client.post(
        urls.add_location_url, test_weather_dict, HTTP_REFERER=urls.referer
    )
    response = auth_client.get(urls.home_url)
    assert response.status_code == 200
    assert "locations" in response.context
    locations = response.context["locations"]
    assert len(locations) > 0


def test_successful_delete_location(auth_client, test_user, test_location):
    location_before = Location.objects.filter(
        user=test_user, name=test_location.name
    ).first()
    assert location_before is not None

    response = auth_client.post(
        urls.delete_url, {"name": test_location.name}, HTTP_REFERER=urls.referer
    )
    assert response.status_code == 302
    assert response.url == urls.referer

    location_after = Location.objects.filter(
        user=test_user, name=test_location.name
    ).first()
    assert location_after is None

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert "удалена" in str(messages[0]).lower()


def test_delete_nonexistent_location(auth_client, test_user):
    non_existent_name = "NonExistentCity_12345"

    assert not Location.objects.filter(user=test_user, name=non_existent_name).exists()

    response = auth_client.post(
        urls.delete_url, {"name": non_existent_name}, HTTP_REFERER=urls.referer
    )

    assert response.status_code == 302
    assert response.url == urls.referer

    messages = list(get_messages(response.wsgi_request))
    error_message = str(messages[0]).lower()
    assert "не найдена" in error_message
    assert non_existent_name in str(messages[0])
