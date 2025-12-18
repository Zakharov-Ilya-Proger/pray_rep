import json
import subprocess

from worker import settings
from worker.model import rec


def transcribe_with_vosk(mp3_path: str) -> str:
    cmd = [
        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
        "-i", mp3_path,
        "-ar", str(settings.SAMPLE_RATE),
        "-ac", "1",
        "-f", "s16le",
        "-"
    ]

    rec.SetWords(True)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        assert p.stdout is not None
        while True:
            data = p.stdout.read(4000)
            if not data:
                break
            rec.AcceptWaveform(data)

        raw = json.loads(rec.FinalResult())
        return raw.get("text", "")
    finally:
        p.kill()
        p.wait()