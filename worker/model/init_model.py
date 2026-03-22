from vosk import Model

from worker.settings import settings

print(f"[STT] loading model from: {settings.MODEL_PATH}")
model = Model(settings.MODEL_PATH)
print("[STT] model loaded")