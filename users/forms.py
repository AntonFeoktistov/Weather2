from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .validators import (
    validate_character_types,
    validate_minimum_length,
    validate_password_max_length,
    validate_username_max_length,
)


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[validate_username_max_length],
        help_text="Обязательное поле.",
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[
            validate_minimum_length,
            validate_character_types,
            validate_password_max_length,
        ],
        help_text="Минимум 2 буквы и 2 цифры",
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Повторите пароль",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        error_messages = {
            "username": {
                "unique": "Пользователь с таким именем уже существует.",
            },
        }

    error_messages = {
        "password_mismatch": "Пароли не совпадают. Пожалуйста, проверьте оба поля.",
    }
