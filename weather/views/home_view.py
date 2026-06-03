from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from weather.errors import WeatherNotFoundError
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
        weather = None
        if form.is_valid():
            try:
                query = form.cleaned_data["query"]
                weather = self.weather_finder.get_weather_by_location_name(query)
            except WeatherNotFoundError:
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
