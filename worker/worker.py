import os
import time
import signal
import redis

from worker.tasks import process

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

QUEUE_KEY = os.getenv("QUEUE_KEY", "stt:queue")
PROCESSING_KEY = os.getenv("PROCESSING_KEY", "stt:processing")
DLQ_KEY = os.getenv("DLQ_KEY", "stt:dlq")

BLOCK_SEC = int(os.getenv("BLOCK_SEC", "5"))
MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", "5"))
ATTEMPTS_HASH = os.getenv("ATTEMPTS_HASH", "stt:attempts")

REQUEUE_ON_START = os.getenv("REQUEUE_ON_START", "1") == "1"

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
        record_id = r.blmove(QUEUE_KEY, PROCESSING_KEY, "LEFT", "RIGHT", timeout=BLOCK_SEC)
        if record_id is None:
            continue

        try:
            process(record_id)
            ack(record_id)
        except Exception as e:
            fail_and_requeue(record_id, str(e))

    except redis.ResponseError as e:
        # если Redis старый и нет BLMOVE
        raise RuntimeError("Redis does not support BLMOVE (needs Redis 6.2+).") from e
    except Exception as e:
        print("ERROR:", e)
        time.sleep(1)

print("Stopped")
