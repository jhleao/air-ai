from fastapi import APIRouter, FastAPI

from .rest.air.router import air_router

router = APIRouter(prefix="/rest/v1")
router.include_router(air_router, tags=["Air"], prefix="/air")

app = FastAPI()
app.include_router(router)
