from django.contrib import admin
from django.urls import include, path
from weather.views.home_view import HomeView

app_name = "weather"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
