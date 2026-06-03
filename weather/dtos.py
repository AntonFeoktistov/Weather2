from pydantic import BaseModel


class LocationDto(BaseModel):
    name_en: str = ""
    name_ru: str = ""
    lon: float = 0.0
    lat: float = 0.0


class WeatherDto(BaseModel):
    location: LocationDto
    temperature: float = 0.0
    description: str = ""
    wind_speed: float = 0.0


def to_dto(dto_class: BaseModel, data: dict):
    return dto_class.model_validate(data)
