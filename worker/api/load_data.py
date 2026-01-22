import tempfile

import requests
from os import close

from worker import settings


def download_mp3(record_id: str) -> str:
    url = settings.API_RECORD_URL + f"?roomID={record_id}"

    resp = requests.post(url, json={"pass": settings.API_RECORD_PASS}, stream=True, timeout=(5, 120))
    resp.raise_for_status()

    fd, path = tempfile.mkstemp(suffix=".webm")
    close(fd)

    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 256):
            if chunk:
                f.write(chunk)
    return path

if __name__ == '__main__':
    print(download_mp3("2716568102"))
