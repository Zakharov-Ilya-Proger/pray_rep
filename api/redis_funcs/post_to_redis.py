import json

from fastapi import HTTPException
from redis import RedisError

from api import settings
from api.redis_client import redis_client


async def post_to_redis(data):
    if redis_client is None:
        raise HTTPException(status_code=503, detail="Redis is not available")

    try:
        payload = json.dumps({"id": data.id}, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=422, detail=f"JSON serialization error: {e}")

    try:
        new_len = await redis_client.rpush(settings.QUEUE_KEY, payload)
        return int(new_len)
    except RedisError as e:
        raise HTTPException(status_code=503, detail=f"Redis error: {e}")
