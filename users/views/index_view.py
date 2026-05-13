from django.shortcuts import render, redirect
from django.views import View

from weather.models import Location


class IndexView(View):
    def get(self, request):
        locations = Location.objects.order_by("-weather_updated_at")[:10]
        return render(request, "users/index.html", {"locations": locations})
