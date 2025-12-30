from redis.asyncio import Redis

redis_client: Redis = Redis(
    host='redis-container',
    port=6379,
)