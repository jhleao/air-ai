from typing import Annotated
from fastapi import APIRouter, Query, Response
from . import service
from ...schema import LatLng, AirAiResponse, UnavailableUserLocationError


air_router = APIRouter()


@air_router.get("/", tags=["Air"], name="Get info about air quality")
async def ask_air(
    response: Response,
    prompt: Annotated[str, Query(max_length=200)],
    lat: Annotated[str | None, Query(max_length=30)] = None,
    lng: Annotated[str | None, Query(max_length=30)] = None,
) -> AirAiResponse | dict:
    if prompt is None:
        # FastAPI handles this already. But mypy doesn't know
        raise ValueError("prompt cannot be empty")

    lat_lng = None

    if lat is not None and lng is not None:
        lat_lng = LatLng(lat=float(lat), lng=float(lng))

    try:
        return await service.prompt_ai(prompt, lat_lng)
    except UnavailableUserLocationError:
        response.status_code = 422
        return {
            "code": "ERR_NO_USER_LOCATION",
            "message": "Unable to find your location. Please provide valid coordinates.",
        }
