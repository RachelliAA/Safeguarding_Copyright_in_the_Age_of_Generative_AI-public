from pydantic import BaseModel, validator, root_validator
from typing import Optional


def normalize_value(value: Optional[str]) -> Optional[str]:
    if isinstance(value, str) and value.strip().lower() in {"none", "n/a"}:
        return None
    return value


class CharacterDescription(BaseModel):
    hairstyle: Optional[str] = None
    outfit: Optional[str] = None
    accessories: Optional[str] = None
    color_scheme: Optional[str] = None
    facial_features: Optional[str] = None
    expression: Optional[str] = None
    pose: Optional[str] = None
    body_proportions: Optional[str] = None

    _normalize = validator('*', allow_reuse=True, pre=True)(normalize_value)


class SceneDescription(BaseModel):
    location: Optional[str] = None
    lighting: Optional[str] = None
    objects_present: Optional[str] = None
    weather: Optional[str] = None

    _normalize = validator('*', allow_reuse=True, pre=True)(normalize_value)


class BuildingDescription(BaseModel):
    architecture_style: Optional[str] = None
    windows: Optional[str] = None
    doors: Optional[str] = None
    landmark_name: Optional[str] = None

    _normalize = validator('*', allow_reuse=True, pre=True)(normalize_value)


class VehicleDescription(BaseModel):
    vehicle_type: Optional[str] = None
    brand_logos: Optional[str] = None
    color: Optional[str] = None
    license_plate: Optional[str] = None

    _normalize = validator('*', allow_reuse=True, pre=True)(normalize_value)


from typing import Optional, Union

class CelebrityDescription(BaseModel):
    name: Optional[str] = None
    facial_similarity_score: Optional[float] = None
    age_estimation: Optional[Union[int, str]] = None  # can be int or str
    quotes: Optional[str] = None

    @validator('name', 'quotes', pre=True)
    def normalize_strings(cls, v):
        return normalize_value(v)

    @validator('facial_similarity_score', pre=True)
    def normalize_facial_similarity_score(cls, v):
        if isinstance(v, str) and v.strip().lower() in {"none", "n/a"}:
            return None
        return v

    @validator('age_estimation', pre=True)
    def normalize_age_estimation(cls, v):
        if isinstance(v, str) and v.strip().lower() in {"none", "n/a"}:
            return None
        # optionally: convert numeric strings to int
        if isinstance(v, str) and v.isdigit():
            return int(v)
        return v



class ImageDescription(BaseModel):
    asset_type: Optional[str] = None
    character: Optional[CharacterDescription] = None
    scene: Optional[SceneDescription] = None
    building: Optional[BuildingDescription] = None
    vehicle: Optional[VehicleDescription] = None
    celebrity: Optional[CelebrityDescription] = None

    @validator('asset_type', pre=True)
    def normalize_asset_type(cls, v):
        return normalize_value(v)

    @root_validator(pre=True)
    def replace_empty_dicts_with_none(cls, values):
        for key in ['character', 'scene', 'building', 'vehicle', 'celebrity']:
            if key in values and isinstance(values[key], dict) and not values[key]:
                values[key] = None
        return values
