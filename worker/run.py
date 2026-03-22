from redis import Redis
from rq import Worker

from worker.settings import settings

from worker.model.init_model import model # noqa: F401
from worker.jobs import process_request # noqa: F401


def main() -> None:
    conn = Redis.from_url(settings.REDIS)
    worker = Worker([settings.QUEUE_KEY], connection=conn)
    worker.work()

if __name__ == "__main__":
    main()
