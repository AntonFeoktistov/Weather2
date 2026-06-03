from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View

from weather.dtos import LocationCreateSchema
from weather.models import Location


class AddLocationView(LoginRequiredMixin, View):
    def post(self, request):
        location_dto, error = self._validate_params(request)

        if error:
            messages.warning(request, error)
            return redirect(request.META.get("HTTP_REFERER", "weather:home"))

        is_location_already_exists = Location.objects.filter(
            user=request.user, name=location_dto.name
        ).first()

        if is_location_already_exists:
            messages.warning(
                request, f'Локация "{location_dto.name}" уже есть в вашем списке'
            )
        else:
            weather = {
                "temperature": location_dto.temperature,
                "description": location_dto.description,
                "wind_speed": location_dto.wind_speed,
            }
            Location.objects.create(
                user=request.user,
                name=location_dto.name,
                lat=location_dto.lat,
                lon=location_dto.lon,
                weather_data=weather,
                weather_updated_at=timezone.now(),
            )
            messages.success(request, f'Локация "{location_dto.name}" добавлена')

        return redirect(request.META.get("HTTP_REFERER", "weather:home"))

    def _validate_params(self, request):
        try:
            dto = LocationCreateSchema(
                name=request.POST.get("name"),
                lat=request.POST.get("lat"),
                lon=request.POST.get("lon"),
                temperature=request.POST.get("temperature"),
                description=request.POST.get("description"),
                wind_speed=request.POST.get("wind_speed"),
            )
            return dto, None
        except Exception as e:
            errors = e.errors()
            first_error = errors[0] if errors else {}
            error_msg = first_error.get("msg", "Неверный формат данных")
            return None, error_msg
