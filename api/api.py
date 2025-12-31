from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import router


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"]
)

api.include_router(router, prefix="/add")
