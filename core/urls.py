from django.contrib import admin
from django.urls import include, path
from weather.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls", namespace="users")),
    path("home/", include("weather.urls", namespace="weather")),
]
