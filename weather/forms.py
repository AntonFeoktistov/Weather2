from django import forms


class LocationSearchForm(forms.Form):
    query = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "search-input",
                "placeholder": "Введите название города или локации...",
                "autocomplete": "off",
            }
        ),
    )
