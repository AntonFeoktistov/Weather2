import pytest
from django.contrib.auth import get_user_model

from tests.urls import urls

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_login_success(client, test_user):
    response = client.post(
        urls.login_url,
        {
            "username": "testuser",
            "password": "testpass123",
        },
    )

    user = User.objects.get(username="testuser")
    assert response.wsgi_request.user.is_authenticated


def test_login_page_accessible(client):
    response = client.get(urls.login_url)
    assert response.status_code == 200
    assert "users/login.html" in response.template_name


def test_authenticated_user_redirected_to_home(client, test_user):
    client.login(username="testuser", password="testpass123")
    response = client.get(urls.login_url)
    assert response.status_code == 302
    assert response.url == urls.home_url


def test_successful_login_redirects_to_home(client, test_user):
    response = client.post(
        urls.login_url, {"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 302
    assert response.url == urls.home_url

    assert response.wsgi_request.user.is_authenticated


def test_failed_login_shows_error(client, test_user):
    response = client.post(
        urls.login_url, {"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors

    assert not response.wsgi_request.user.is_authenticated


def test_inactive_user_cannot_login(client, test_user):
    test_user.is_active = False
    test_user.save()

    response = client.post(
        urls.login_url, {"username": "testuser", "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors

    assert not response.wsgi_request.user.is_authenticated


# logout


def test_logout_requires_post(
    client,
    test_user,
):
    client.login(username="testuser", password="testpass123")

    response = client.get(urls.logout_url)
    assert response.status_code == 405
    assert response.wsgi_request.user.is_authenticated


def test_successful_logout_redirects_to_home(client, test_user):
    client.login(username="testuser", password="testpass123")
    assert client.session.get("_auth_user_id") is not None

    response = client.post(urls.logout_url)
    assert response.status_code == 302
    assert response.url == urls.home_url

    assert client.session.get("_auth_user_id") is None


def test_logout_redirects_to_home_even_if_not_logged_in(client):
    response = client.post(urls.logout_url)
    assert response.status_code == 302
    assert response.url == urls.home_url
