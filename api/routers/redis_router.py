from fastapi import APIRouter, HTTPException
from api import reqModel, post_to_redis

router = APIRouter(
    tags=['Post Audio'],
)

@router.post(
    '/redis',
    responses={
        201: {"description": "Successfully added"},
        400: {"description": "Bad Request"},
        409: {"description": "Key already exists"},
        422: {"description": "Unprocessable Entity"},
        500: {"description": "Internal Server Error"},
    }
)
async def post_audio(request: reqModel):
    res = await post_to_redis(request)
    if not isinstance(res, HTTPException):
        return {"ok": True, "queue": "settings.QUEUE_KEY", "new_length": res}
    raise res
