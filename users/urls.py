from django.contrib import admin
from django.urls import include, path
from users.views.index_view import IndexView
from users.views.log_in_out_view import CustomLoginView, CustomLogoutView
from users.views.register_view import RegisterView

app_name = "users"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    
    
]