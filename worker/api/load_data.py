import tempfile

import requests
from os import close

from worker import settings


def download_mp3(hash: str) -> str:
    url = settings.API_RECORD_URL

    resp = requests.get(url+f'/{hash}', stream=True)
    resp.raise_for_status()

    fd, path = tempfile.mkstemp(suffix=".webm")
    close(fd)

    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 256):
            if chunk:
                f.write(chunk)
    return path


if __name__ == '__main__':
    print(download_mp3("1767103126"))
