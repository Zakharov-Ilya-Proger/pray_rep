from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from api import router, settings


redis_client: Redis | None = None

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"]
)

@api.on_event("startup")
async def startup():
    global redis_client
    redis_client = Redis.from_url(settings.REDIS, decode_responses=True)


@api.on_event("shutdown")
async def shutdown():
    if redis_client:
        await redis_client.close()

api.include_router(router, prefix="/add")
