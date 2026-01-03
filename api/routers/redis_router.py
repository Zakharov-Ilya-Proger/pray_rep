from fastapi import APIRouter, HTTPException

from api.models.reqModel import reqModel
from api.redis_funcs.post_to_redis import post_to_redis
from api.settings import settings
from api.api_pass import check_password

router = APIRouter(
    tags=['Post Audio'],
)

@router.post(
    '/redis',
    responses={
        201: {"description": "Successfully added"},
        401: {"description": "Unauthorized"},
        400: {"description": "Bad Request"},
        409: {"description": "Key already exists"},
        422: {"description": "Unprocessable Entity"},
        500: {"description": "Internal Server Error"},
    }
)
async def post_audio(request: reqModel):
    auth = await check_password(request.api_pass, settings.API_PASS)
    res = await post_to_redis(request.id)
    if not isinstance(res, HTTPException):
        return {"ok": True, "queue": settings.QUEUE_KEY, "job_id": res}
    raise res
