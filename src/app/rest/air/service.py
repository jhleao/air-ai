from ...schema import LatLng, AirAiResponse
from ...ai import AirAi


async def prompt_ai(user_query: str, user_lat_lng: LatLng | None) -> AirAiResponse:
    return await AirAi(user_lat_lng).acall(user_query)
