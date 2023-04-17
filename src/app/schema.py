from pydantic import BaseModel
from typing import List


class LatLng(BaseModel):
    lat: float = 0
    lng: float = 0


class Place(BaseModel):
    name: str
    state: str
    country_code: str


class AirDataPoint(BaseModel):
    date_unix: int
    aqi: float
    pm2_5: float
    o3: float
    co: float
    no: float
    no2: float
    so2: float
    pm10: float
    nh3: float


class LocationAirData(BaseModel):
    location_name: str
    data: List[AirDataPoint]


class AirAiResponse(BaseModel):
    answer: str
    facts: List[str] | None
    auxiliary_data: List[LocationAirData] | None


class PlaceNotFoundError(Exception):
    pass


class UnavailableUserLocationError(Exception):
    pass
