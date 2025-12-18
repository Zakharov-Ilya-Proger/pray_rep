import tempfile

import requests
from os import close

from worker import settings


def download_mp3(record_id: str) -> str:
    """
    Скачиваем mp3 во временный файл (стримом).
    Вернём путь к файлу.
    """
    url = f"{settings.AUDIO_API_BASE}/records/{record_id}/mp3"
    headers = {}
    if settings.AUDIO_API_TOKEN:
        headers["Authorization"] = f"Bearer {settings.AUDIO_API_TOKEN}"

    resp = requests.get(url, headers=headers, stream=True, timeout=(5, 120))
    resp.raise_for_status()

    fd, path = tempfile.mkstemp(suffix=".mp3")
    close(fd)

    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 256):
            if chunk:
                f.write(chunk)
    return path