import anyio
from fastapi import HTTPException
from rq import Retry

from api.redis_client import queue
from api import settings

async def post_to_redis(req_id: str):
    try:
        def _enqueue():
            return queue.enqueue(
                "worker.jobs.process_request",
                req_id,
                retry=Retry(max=settings.settings.MAX_ATTEMPTS, interval=[1, 5, 15]),
                job_timeout=-1,
                result_ttl=0,
                failure_ttl=7 * 24 * 3600,
            )

        job = await anyio.to_thread.run_sync(_enqueue)
        return {"job_id": job.id}

    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Queue error: {e}")
