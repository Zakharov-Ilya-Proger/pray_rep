import tempfile

import requests
from os import close

from worker import settings


def download_mp3(hash: str) -> str:
    url = settings.API_RECORD_URL +f'/{hash}'
    with requests.Session() as session:
        with session.get(url, stream=True) as resp:
            resp.raise_for_status()

            fd, temp_path = tempfile.mkstemp(
                suffix=".webm",
                dir=settings.DOWNLOAD_DIR,
            )
            close(fd)

            with open(temp_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

    return temp_path


if __name__ == '__main__':
    print(download_mp3("1767103126"))
