from dataclasses import asdict
from urllib.parse import quote
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from weather.forms import LocationSearchForm
from weather.weather_finder import WeatherFinder


class HomeView(LoginRequiredMixin, View):
    template_name = "weather/home.html"
    login_url = "users:login"
    redirect_field_name = "next"
    weather_finder = WeatherFinder()

    def get(self, request):
        form = LocationSearchForm()
        locations = ["loc1", "loc2", "loc3"]
        return render(
            request,
            self.template_name,
            {
                "locations": locations,
                "form": form,
            },
        )

    def post(self, request):
        locations = ["loc1", "loc2", "loc3"]
        form = LocationSearchForm(request.POST)
        query = ""
        if form.is_valid():
            query = form.cleaned_data["query"]
            weather = self.weather_finder.get_weather_by_location_name(query)
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
