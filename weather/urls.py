from django.urls import path

from weather.views.add_location_view import AddLocationView
from weather.views.delete_location_view import DeleteLocationView
from weather.views.home_view import HomeView
from weather.views.refresh_weather_view import RefreshWeatherView

app_name = "weather"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("add_location", AddLocationView.as_view(), name="add_location"),
    path("delete_location", DeleteLocationView.as_view(), name="delete_location"),
    path("refresh_weather", RefreshWeatherView.as_view(), name="refresh_weather"),
]
