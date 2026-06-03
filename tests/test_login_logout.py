import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

login_url = reverse("users:login")
logout_url = reverse("users:logout")
home_url = reverse("users:home")
User = get_user_model()

pytestmark = pytest.mark.django_db


def test_login_success(client):

    response = client.post(
        login_url,
        {
            "username": "newuser",
            "password1": "pass123",
            "password2": "pass123",
        },
    )

    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()
    assert response.url == reverse("users:index")


def test_login_page_accessible(self, client):
    response = client.get(login_url)
    assert response.status_code == 200
    assert "users/login.html" in response.template_name


def test_authenticated_user_redirected_to_home(self, client, test_user):
    client.login(username="testuser", password="testpass123")
    response = client.get(login_url)
    assert response.status_code == 302
    assert response.url == home_url


def test_successful_login_redirects_to_home(self, client, test_user):
    response = client.post(
        login_url, {"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 302
    assert response.url == home_url

    assert response.wsgi_request.user.is_authenticated


def test_failed_login_shows_error(self, client, test_user):
    response = client.post(
        login_url, {"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors

    assert not response.wsgi_request.user.is_authenticated


def test_inactive_user_cannot_login(self, client, test_user):
    test_user.is_active = False
    test_user.save()

    response = client.post(
        login_url, {"username": "testuser", "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors

    assert not response.wsgi_request.user.is_authenticated


# logout


def test_logout_requires_post(
    self,
    client,
    test_user,
):
    client.login(username="testuser", password="testpass123")

    response = client.get(logout_url)
    assert response.status_code == 405
    assert response.wsgi_request.user.is_authenticated


def test_successful_logout_redirects_to_home(self, client, test_user):
    client.login(username="testuser", password="testpass123")
    assert client.session.get("_auth_user_id") is not None

    response = client.post(logout_url)
    assert response.status_code == 302
    assert response.url == home_url

    assert client.session.get("_auth_user_id") is None


def test_logout_redirects_to_home_even_if_not_logged_in(self, client):
    response = client.post(logout_url)
    assert response.status_code == 302
    assert response.url == home_url
