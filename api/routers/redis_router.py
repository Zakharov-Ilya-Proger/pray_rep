from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader

from api.api_pass import check_password
from api.models.reqModel import reqModel
from api.redis_funcs.post_to_redis import post_to_redis
from api.settings import settings

router = APIRouter(
)

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=True,
    description="API ключ для аутентификации. Получить ключ можно у разработчика"
)

@router.post(
    '/redis',
    openapi_extra={
        "security": [{"APIKeyHeader": []}]
    },
    responses={
        401: {"description": "Unauthorized"},
        400: {"description": "Bad Request"},
        409: {"description": "Key already exists"},
        422: {"description": "Unprocessable Entity"},
        500: {"description": "Internal Server Error"},
    },
    summary="Постановка задачи асинхронной обработки аудио в Redis очередь",
    description='''
    Добавляет задачу обработки аудио в Redis очередь для последующей асинхронной обработки.

    Процесс работы:
    1. API проверяет аутентификацию по ключу
    2. Валидирует входные данные
    3. Помещает задачу в Redis очередь
    4. Возвращает идентификатор задачи (job_id)

    Что происходит далее:
    - Рабочий процесс (worker) забирает задачу из очереди
    - Загружает аудиофайл по указанному ID
    - Обрабатывает аудио (транскрибация, анализ и т.д.)
    - Сохраняет результаты в хранилище

    Примечание:
    Статус обработки задачи можно отслеживать по возвращенному job_id через соответствующие эндпоинты.
    Пример запроса:
    
    POST https://net.molitvamira.ru/add/redis
    Content-Type: application/json
    X-API-Key: KEY
    {
      "id": "ID"
    }
        ''',
    response_description="ID задачи в очереди и имя используемой очереди"

)
async def post_audio(request: reqModel, key: str = Depends(api_key_header)):
    auth = await check_password(key)
    if not auth:
        raise HTTPException(401)
    res = await post_to_redis(request.id, request.hash)
    if not isinstance(res, HTTPException):
        return {"ok": True, "queue": settings.QUEUE_KEY, "job_id": res}
    raise res
