from uvicorn import run
from api import api
from api.settings import settings

if __name__ == '__main__':
    run(
        api,
        host='0.0.0.0',
        port=settings.PORT,
        workers=settings.WORKERS,
    )
