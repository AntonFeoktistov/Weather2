from dataclasses import asdict
from urllib.parse import quote
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):
    template_name = "weather/home.html"
    login_url = "users:login"
    redirect_field_name = "next"

    def get(self, request):
        locations = ["loc1", "loc2", "loc3"]
        return render(
            request,
            self.template_name,
            {
                "locations": locations,
            },
        )
