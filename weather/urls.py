from django.contrib import admin
from django.urls import include, path
from weather.views import AddLocationView, DeleteLocationView, HomeView, RefreshWeatherView

app_name = "weather"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("add_location", AddLocationView.as_view(), name="add_location"),
    path("delete_location", DeleteLocationView.as_view(), name="delete_location"),
    path("refresh_weather", RefreshWeatherView.as_view(), name="refresh_weather"),
]
