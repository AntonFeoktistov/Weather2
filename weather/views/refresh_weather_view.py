from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View


class RefreshWeatherView(LoginRequiredMixin, View):
    def post(self, request):

        return redirect(request.META.get("HTTP_REFERER", "weather:home"))
