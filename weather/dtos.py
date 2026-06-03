from pydantic import BaseModel, Field, validator


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


class LocationCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    temperature: float = Field(..., ge=-100, le=60)
    description: str = Field(..., min_length=1)
    wind_speed: float = Field(..., ge=0, le=200)

    @validator("name")
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Название локации не может быть пустым")
        return v.strip()


def to_dto(dto_class: BaseModel, data: dict):
    return dto_class.model_validate(data)
