# tests/test_views.py
import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from weather.models import Location

User = get_user_model()
add_location_url = reverse("weather:add_location")
home_url = reverse("weather:home")
referer_url = reverse("weather:home")
update_url = reverse("weather:refresh_weather")
delete_url = reverse("weather:delete_location")
pytestmark = pytest.mark.django_db


def test_unauthenticated_user_cannot_add_location(client, test_weather_dict):
    response = client.post(add_location_url, test_weather_dict)

    assert response.status_code == 302
    assert response.url.startswith("/login/")
    assert not Location.objects.filter(name=test_weather_dict["name"])


def test_successful_location_addition(self, auth_client, test_user, test_weather_dict):
    response = auth_client.post(
        add_location_url, test_weather_dict, HTTP_REFERER=referer_url
    )

    assert response.status_code == 302
    assert response.url == referer_url

    location = Location.objects.filter(
        user=test_user, name=test_weather_dict["name"]
    ).first()

    assert location is not None
    assert location.lat == test_weather_dict["lat"]
    assert location.lon == test_weather_dict["lon"]
    assert location.weather_data["temperature"] == test_weather_dict["temperature"]
    assert location.weather_data["description"] == test_weather_dict["description"]
    assert location.weather_data["wind_speed"] == test_weather_dict["wind_speed"]
    assert location.weather_updated_at is not None

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0
    assert "добавлена" in str(messages[0])


def test_add_duplicate_location(
    auth_client, test_user, test_location, test_weather_dict
):
    response = auth_client.post(
        add_location_url, test_weather_dict, HTTP_REFERER=referer_url
    )
    response = auth_client.post(
        add_location_url, test_weather_dict, HTTP_REFERER=referer_url
    )
    assert (
        Location.objects.filter(user=test_user, name=test_weather_dict["name"]).count()
        == 1
    )
    messages = list(get_messages(response.wsgi_request))
    assert any("уже" in str(m) for m in messages)


def test_missing_required_fields(self, auth_client):
    response = auth_client.post(
        add_location_url,
        {
            "name": "Berlin",
        },
        HTTP_REFERER=referer_url,
    )
    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    assert any("Неверный формат" in str(m) for m in messages)


# READ
def test_get_locations_unauthorized(client):
    response = client.get(home_url)

    assert response.status_code == 302
    assert response.url.startswith("/login/")


def test_get_locations(auth_client, test_weather_dict):

    response = auth_client.post(
        add_location_url, test_weather_dict, HTTP_REFERER=referer_url
    )
    response = auth_client.get(home_url)
    assert response.status_code == 200
    assert "locations" in response.context
    locations = response.context["locations"]
    assert len(locations) > 0


# UPDATE TODO MOCK for openweather

# DELETE


def test_successful_delete_location(self, auth_client, test_user, test_location):
    location_before = Location.objects.filter(
        user=test_user, name=test_location.name
    ).first()
    assert location_before is not None

    response = auth_client.post(
        delete_url, {"name": test_location.name}, HTTP_REFERER=referer_url
    )
    assert response.status_code == 302
    assert response.url == referer_url

    location_after = Location.objects.filter(
        user=test_user, name=test_location.name
    ).first()
    assert location_after is None

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert "удалена" in str(messages[0]).lower()


def test_delete_nonexistent_location(self, auth_client, test_user):
    non_existent_name = "NonExistentCity_12345"

    assert not Location.objects.filter(user=test_user, name=non_existent_name).exists()

    response = auth_client.post(
        delete_url, {"name": non_existent_name}, HTTP_REFERER=referer_url
    )

    assert response.status_code == 302
    assert response.url == referer_url

    messages = list(get_messages(response.wsgi_request))
    error_message = str(messages[0]).lower()
    assert "не найдена" in error_message
    assert non_existent_name in str(messages[0])
