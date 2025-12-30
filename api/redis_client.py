from redis.asyncio import Redis

from api.settings import settings

redis = Redis()
redis_client = redis.from_url(settings.REDIS)