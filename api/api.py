from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.redis_client import redis_client
from api.routers import router
from api.settings import settings


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"]
)

@api.on_event("startup")
async def startup():
    redis_client.from_url(settings.REDIS, decode_responses=True)


@api.on_event("shutdown")
async def shutdown():
    if redis_client:
        await redis_client.close()

api.include_router(router, prefix="/add")
