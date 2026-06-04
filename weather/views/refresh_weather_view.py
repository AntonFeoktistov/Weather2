from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View

from weather.errors import WeatherNotFoundError
from weather.models import Location
from weather.weather_finder import WeatherFinder


class RefreshWeatherView(LoginRequiredMixin, View):
    weather_finder = WeatherFinder()

    def post(self, request):
        locations = Location.objects.filter(user=request.user)
        for location in locations:
            try:
                weather = self.weather_finder.get_weather_by_location_name(
                    location.name
                )

                weather_data = {
                    "temperature": weather.temperature,
                    "description": weather.description,
                    "wind_speed": weather.wind_speed,
                }

                location.weather_data = weather_data
                location.weather_updated_at = timezone.now()
                location.save()

            except WeatherNotFoundError:
                continue

        return redirect(request.META.get("HTTP_REFERER", "weather:home"))
