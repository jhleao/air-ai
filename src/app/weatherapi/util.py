import datetime
from collections import defaultdict
from functools import reduce
from typing import Callable, List, TypeVar

from ..schema import AirDataPoint

T = TypeVar("T")


class OpenWeatherMapUtils:
    @staticmethod
    def reduce_air_data_points_by_day(points: List[AirDataPoint]) -> List[AirDataPoint]:
        """Groups and reduces data points by day. Could make this more generic in the future"""

        def reduce_points(
            air_data_1: AirDataPoint, air_data_2: AirDataPoint
        ) -> AirDataPoint:
            return AirDataPoint(
                aqi=(air_data_1.aqi + air_data_2.aqi) / 2,
                o3=(air_data_1.o3 + air_data_2.o3) / 2,
                pm2_5=(air_data_1.pm2_5 + air_data_2.pm2_5) / 2,
                co=(air_data_1.co + air_data_2.co) / 2,
                date_unix=air_data_1.date_unix,
            )

        def get_point_day(air_data: AirDataPoint) -> str:
            date = datetime.datetime.fromtimestamp(air_data.date_unix).date()
            return f"{date.day}{date.month}{date.year}"

        def group_by_hash(objects: List[T], hash: Callable[[T], str]) -> List[List[T]]:
            grouped_objects = defaultdict(list)
            for obj in objects:
                hash_value = hash(obj)
                grouped_objects[hash_value].append(obj)
            return list(grouped_objects.values())

        def reduce_2d(array: List[List[T]], reducer: Callable[[T, T], T]) -> List[T]:
            return [reduce(reducer, row) if len(row) > 1 else row[0] for row in array]

        grouped_points = group_by_hash(points, get_point_day)
        reduced_points = reduce_2d(grouped_points, reduce_points)

        return reduced_points

    @staticmethod
    def calculate_aqi_pm2_5(concentration: float) -> int:
        """
        This function is based on airnow.gov's AQI calculation.
        Including the breakpoints and reference values.
        Since they are is also the reference values we're instructing the model with in the prompts
        https://www.airnow.gov/aqi/aqi-calculator-concentration/
        """
        aqi = float(concentration)
        aqi = (int(10 * aqi)) / 10

        if 0 <= aqi < 12.1:
            aqi = OpenWeatherMapUtils.linear_interpolation(50, 0, 12, 0, aqi)
        elif 12.1 <= aqi < 35.5:
            aqi = OpenWeatherMapUtils.linear_interpolation(100, 51, 35.4, 12.1, aqi)
        elif 35.5 <= aqi < 55.5:
            aqi = OpenWeatherMapUtils.linear_interpolation(150, 101, 55.4, 35.5, aqi)
        elif 55.5 <= aqi < 150.5:
            aqi = OpenWeatherMapUtils.linear_interpolation(200, 151, 150.4, 55.5, aqi)
        elif 150.5 <= aqi < 250.5:
            aqi = OpenWeatherMapUtils.linear_interpolation(300, 201, 250.4, 150.5, aqi)
        elif 250.5 <= aqi < 350.5:
            aqi = OpenWeatherMapUtils.linear_interpolation(400, 301, 350.4, 250.5, aqi)
        elif 350.5 <= aqi < 500.5:
            aqi = OpenWeatherMapUtils.linear_interpolation(500, 401, 500.4, 350.5, aqi)
        else:
            aqi = 0

        return aqi

    @staticmethod
    def linear_interpolation(
        aqi_high: float,
        aqi_low: float,
        conc_high: float,
        conc_low: float,
        conc: float,
    ) -> int:
        a = ((conc - conc_low) / (conc_high - conc_low)) * (aqi_high - aqi_low) + aqi_low
        linear_aqi = round(a)
        return linear_aqi
