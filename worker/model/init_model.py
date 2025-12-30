from vosk import Model, KaldiRecognizer, SetLogLevel
from worker import settings

model = Model("C:\\Users\\User\\Downloads\\vosk-model-ru-0.42")
rec = KaldiRecognizer(model, 16000)
