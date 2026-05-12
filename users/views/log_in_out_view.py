from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):

    template_name = "users/login.html"
    redirect_authenticated_user = True
    next_page = "weather:home"


class CustomLogoutView(LogoutView):
    next_page = "weather:home"
