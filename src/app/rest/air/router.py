from typing import Annotated
from fastapi import APIRouter, Query
from . import service

air_router = APIRouter()


@air_router.get("/", tags=["Air"], name="Get info about air quality")
async def ask_air(
    prompt: Annotated[str, Query(max_length=200)],
) -> dict:
    return await service.prompt_ai(prompt)
