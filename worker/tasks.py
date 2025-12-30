from worker.api import download_mp3, post_data
from worker.model import transcribe_with_vosk
from os import path, remove


def process(record_id: str) -> None:
    mp3_path = None
    print(record_id)
    try:
        mp3_path = download_mp3(record_id)
        text = transcribe_with_vosk(mp3_path)
        post_data(record_id, text)
    finally:
        if mp3_path and path.exists(mp3_path):
            try:
                remove(mp3_path)
            except Exception:
                pass
