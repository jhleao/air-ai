import asyncio
import atexit
import os
from typing import List

from aiohttp import ClientSession

from ..etc.singleton import singleton
from ..schema import AirDataPoint, LatLng, Place, PlaceNotFoundError
from .util import OpenWeatherMapUtils


@singleton
class OpenWeatherMapApi:
    api_key: str | None = None
    session: ClientSession = ClientSession("http://api.openweathermap.org/")

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        atexit.register(asyncio.run, self.session.close())

    async def geocode(self, place_name: str) -> LatLng:
        url = "/geo/1.0/direct"
        params = {"q": place_name, "appid": self.api_key}
        async with self.session.get(url, params=params) as response:
            data = await response.json()
            if len(data) == 0:
                raise PlaceNotFoundError()
            first_result: dict[str, float] = data[0]
            lat = first_result.get("lat")
            lng = first_result.get("lon")
            assert lat is not None
            assert lng is not None
            return LatLng(lat=lat, lng=lng)

    async def rev_geocode(self, lat_lng: LatLng) -> Place:
        url = "/geo/1.0/reverse"
        params = {
            "lat": lat_lng.lat,
            "lon": lat_lng.lng,
            "limit": 1,
            "appid": self.api_key,
        }
        async with self.session.get(url, params=params) as response:
            data = await response.json()
            first_result: dict[str, str] = data[0]
            place = first_result.get("name")
            state = first_result.get("state")
            country_code = first_result.get("country")
            assert place is not None
            assert state is not None
            assert country_code is not None
            return Place(name=place, state=state, country_code=country_code)

    async def air_quality(
        self, lat_lng: LatLng, start_unix: int, end_unix: int
    ) -> List[AirDataPoint]:
        url = "/data/2.5/air_pollution/history"
        params = {
            "lat": lat_lng.lat,
            "lon": lat_lng.lng,
            "start": start_unix,
            "end": end_unix,
            "appid": self.api_key,
        }
        async with self.session.get(url, params=params) as response:
            data = await response.json()
            formatted_data = []
            for data_point in data.get("list"):
                date_unix = data_point.get("dt")
                aqi = OpenWeatherMapUtils.calculate_aqi_pm2_5(
                    data_point.get("components").get("pm2_5")
                )
                pm2_5 = round(data_point.get("components").get("pm2_5"), 2)
                o3 = round(data_point.get("components").get("o3"), 2)
                co = round(data_point.get("components").get("co"), 2)
                formatted = AirDataPoint(
                    date_unix=date_unix, aqi=aqi, pm2_5=pm2_5, o3=o3, co=co
                )
                formatted_data.append(formatted)

            # We always want them by day. OWM only provides hour granularity
            return OpenWeatherMapUtils.reduce_air_data_points_by_day(formatted_data)
