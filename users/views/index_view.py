from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("weather:home")
        locations = ["loc1", "loc2", "loc3"]
        return render(request, "users/index.html", {"locations": locations})
