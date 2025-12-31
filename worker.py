import os
import time
import signal
import redis

from worker import settings
from worker.tasks import process

REDIS_URL = settings.REDIS_URL

QUEUE_KEY = settings.QUEUE_KEY
PROCESSING_KEY = settings.PROCESSING_KEY
DLQ_KEY = settings.DLQ_KEY

BLOCK_SEC = settings.BLOCK_SEC
MAX_ATTEMPTS = settings.MAX_ATTEMPTS
ATTEMPTS_HASH = settings.ATTEMPTS_HASH

REQUEUE_ON_START = settings.REQUEUE_ON_START

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
stop = False

def handle_sig(_signum, _frame):
    global stop
    stop = True

signal.signal(signal.SIGINT, handle_sig)
signal.signal(signal.SIGTERM, handle_sig)

def ack(record_id: str) -> None:
    r.lrem(PROCESSING_KEY, 1, record_id)
    r.hdel(ATTEMPTS_HASH, record_id)

def fail_and_requeue(record_id: str, err: str) -> None:
    attempt = r.hincrby(ATTEMPTS_HASH, record_id, 1)
    r.lrem(PROCESSING_KEY, 1, record_id)

    if attempt >= MAX_ATTEMPTS:
        r.rpush(DLQ_KEY, record_id)
        print(f"DLQ {record_id} after {attempt} attempts. err={err}")
        return

    r.rpush(QUEUE_KEY, record_id)
    print(f"REQUEUE {record_id} attempt={attempt} err={err}")

def requeue_leftovers_on_start():
    while True:
        x = r.lpop(PROCESSING_KEY)
        if x is None:
            break
        r.rpush(QUEUE_KEY, x)
    print("Requeued leftovers from processing")

if REQUEUE_ON_START:
    requeue_leftovers_on_start()

while not stop:
    try:
        record_id = r.blmove(QUEUE_KEY, PROCESSING_KEY, src="LEFT", dest="RIGHT", timeout=BLOCK_SEC)
        print(record_id)
        if record_id is None:
            continue

        try:
            process(record_id['id'])
            ack(record_id)
        except Exception as e:
            fail_and_requeue(record_id, str(e))

    except redis.ResponseError as e:
        raise RuntimeError("Redis does not support BLMOVE (needs Redis 6.2+).") from e
    except Exception as e:
        print("ERROR:", e)
        time.sleep(1)

print("Stopped")
