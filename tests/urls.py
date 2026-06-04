from dataclasses import dataclass

from django.urls import reverse


@dataclass(frozen=True, slots=True)
class Urls:
    home_url: str
    add_location_url: str
    delete_url: str
    refresh_url: str
    login_url: str
    logout_url: str
    register_url: str

    @property
    def referer(self) -> str:
        return self.home_url


urls = Urls(
    home_url=reverse("weather:home"),
    add_location_url=reverse("weather:add_location"),
    delete_url=reverse("weather:delete_location"),
    refresh_url=reverse("weather:refresh_weather"),
    login_url=reverse("users:login"),
    logout_url=reverse("users:logout"),
    register_url=reverse("users:register"),
)
