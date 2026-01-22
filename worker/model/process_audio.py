import json
import subprocess

from vosk import KaldiRecognizer

from worker.model.init_model import model


def transcribe_with_vosk(mp3_path: str) -> str:
    cmd = [
        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
        "-i", mp3_path,
        "-vn",
        "-map", "0:a:0",
        "-acodec", "pcm_s16le",
        "-ar", 16000,
        "-ac", "1",
        "-f", "s16le",
        "pipe:1"
    ]
    rec = KaldiRecognizer(model, 16000)

    rec.SetWords(False)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        CHUNK = 32000 * 2
        assert p.stdout is not None
        while True:
            data = p.stdout.read(CHUNK)
            if not data:
                break
            rec.AcceptWaveform(data)
        raw = json.loads(rec.FinalResult())
        return raw.get("text", "")
    finally:
        p.kill()
        p.wait()
