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
    },
    description='''
    Adding to Redis Queue endpoint. Worker will take the job from queue, load audio n process it 
    '''
)
async def post_audio(request: reqModel):
    auth = await check_password(request.api_pass)
    if not auth:
        raise HTTPException(401)
    res = await post_to_redis(request.id)
    if not isinstance(res, HTTPException):
        return {"ok": True, "queue": settings.QUEUE_KEY, "job_id": res}
    raise res
