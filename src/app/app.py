from dotenv import load_dotenv


from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .rest.air.router import air_router

load_dotenv()


router = APIRouter(prefix="/rest/v1")
router.include_router(air_router, tags=["Air"], prefix="/air")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
