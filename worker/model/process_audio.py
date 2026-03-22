import json
import subprocess

from vosk import KaldiRecognizer

from worker.model.init_model import model


def transcribe_with_vosk(mp3_path: str) -> str:
    cmd = [
        "ffmpeg",
        "-nostdin",
        "-hide_banner",
        "-loglevel", "error",
        "-i", mp3_path,
        "-vn",
        "-map", "0:a:0",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-f", "s16le",
        "pipe:1",
    ]

    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(False)
    rec.SetPartialWords(False)
    rec.SetMaxAlternatives(0)

    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=10**6,
    )

    try:
        chunk_size = 65536

        assert p.stdout is not None

        while True:
            data = p.stdout.read(chunk_size)
            if not data:
                break
            rec.AcceptWaveform(data)

        return json.loads(rec.FinalResult()).get("text", "")
    finally:
        if p.poll() is None:
            p.kill()
        p.wait()
