import os
import subprocess
import time
from os import path, remove

from worker.api.load_data import download_mp3
from worker.api.post_data import post_data
from worker.model.process_audio import transcribe_with_vosk


def get_audio_duration_sec(file_path: str) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path,
        ],
        text=True,
    ).strip()
    return float(out)


def process(record_id: str, hash: str) -> None:
    mp3_path = None

    print(f"[STT] start room_id={record_id} hash={hash}")

    try:
        t0 = time.perf_counter()
        mp3_path = download_mp3(hash)
        t1 = time.perf_counter()

        size_mb = os.path.getsize(mp3_path) / 1024 / 1024
        duration_sec = get_audio_duration_sec(mp3_path)

        print(
            f"[STT] downloaded file={mp3_path} "
            f"size={size_mb:.2f}MB duration={duration_sec:.2f}s "
            f"download_time={t1 - t0:.2f}s"
        )

        text = transcribe_with_vosk(mp3_path)
        t2 = time.perf_counter()

        post_data(record_id, text)
        t3 = time.perf_counter()

        rtf = (t2 - t1) / duration_sec if duration_sec > 0 else 0.0

        print(
            f"[STT] done room_id={record_id} "
            f"transcribe_time={t2 - t1:.2f}s "
            f"post_time={t3 - t2:.2f}s "
            f"total_time={t3 - t0:.2f}s "
            f"rtf={rtf:.2f}x "
            f"text_len={len(text)}"
        )

    except Exception as e:
        print(f"[STT] ERROR room_id={record_id} hash={hash}: {e}")
        raise
    finally:
        if mp3_path and path.exists(mp3_path):
            try:
                remove(mp3_path)
                print(f"[STT] temp file removed: {mp3_path}")
            except Exception as e:
                print(f"[STT] temp file remove failed: {mp3_path} error={e}")