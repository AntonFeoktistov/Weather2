from dataclasses import asdict
from django.utils import timezone
from django.contrib import messages
from urllib.parse import quote
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from weather.forms import LocationSearchForm
from weather.models import Location
from weather.weather_finder import WeatherFinder


class HomeView(LoginRequiredMixin, View):
    template_name = "weather/home.html"
    login_url = "users:login"
    redirect_field_name = "next"
    weather_finder = WeatherFinder()

    def get(self, request):
        form = LocationSearchForm()
        locations = Location.objects.filter(user=request.user)
        return render(
            request,
            self.template_name,
            {
                "locations": locations,
                "form": form,
            },
        )

    def post(self, request):
        form = LocationSearchForm(request.POST)
        locations = Location.objects.filter(user=request.user)
        query = ""
        if form.is_valid():
            query = form.cleaned_data["query"]
            weather = self.weather_finder.get_weather_by_location_name(query)
            if weather.description == "":
                weather = None
                messages.warning(request, "Локация не найдена")
        return render(
            request,
            "weather/home.html",
            {
                "locations": locations,
                "form": form,
                "query": query,
                "weather": weather,
            },
        )


class AddLocationView(LoginRequiredMixin, View):

    def post(self, request):
        name = request.POST.get("name")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")
        temperature = request.POST.get("temperature")
        description = request.POST.get("description")
        wind_speed = request.POST.get("wind_speed")

        is_location_already_exists = Location.objects.filter(
            user=request.user, name=name
        ).first()

        if is_location_already_exists:
            messages.warning(request, f'Локация "{name}" уже есть в вашем списке')
        else:
            weather = {
                "temperature": temperature,
                "description": description,
                "wind_speed": wind_speed,
            }
            Location.objects.create(
                user=request.user,
                name=name,
                lat=lat,
                lon=lon,
                weather_data=weather,
                weather_updated_at=timezone.now(),
            )
            messages.success(request, f'Локация "{name}" добавлена')

        return redirect(request.META.get("HTTP_REFERER", "weather:home"))


class DeleteLocationView(LoginRequiredMixin, View):

    def post(self, request):
        name = request.POST.get("name")

        if name:
            deleted_count, _ = Location.objects.filter(
                user=request.user, name=name
            ).delete()

            if deleted_count:
                messages.success(request, f'Локация "{name}" удалена из избранного')
            else:
                messages.warning(request, f'Локация "{name}" не найдена')

        return redirect(request.META.get("HTTP_REFERER", "weather:home"))


class RefreshWeatherView(LoginRequiredMixin, View):

    def post(self, request):

        return redirect(request.META.get("HTTP_REFERER", "weather:home"))
