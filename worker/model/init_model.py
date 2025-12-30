from vosk import Model, KaldiRecognizer, SetLogLevel
from worker import settings

model = Model(settings.MODEL_PATH)
rec = KaldiRecognizer(model, 16000)
