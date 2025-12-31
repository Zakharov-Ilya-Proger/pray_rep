from redis import Redis
from rq import Queue

from api import settings

redis_conn = Redis.from_url(settings.settings.REDIS)
queue = Queue(name=settings.settings.QUEUE_KEY, connection=redis_conn)