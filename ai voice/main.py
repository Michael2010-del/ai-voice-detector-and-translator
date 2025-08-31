import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator


LANGUAGE_CODES = {
    'en': 'английский',
    'es': 'испанский',
    'fr': 'французский',
    'de': 'немецкий',
    'it': 'итальянский',
    'pt': 'португальский',
    'zh': 'китайский',
    'ja': 'японский',
    'ko': 'корейский',
    'ar': 'арабский',
    'hi': 'хинди',
    'tr': 'турецкий',
    'nl': 'голландский',
    'el': 'греческий',
    'he': 'иврит'
}


duration = 5  # секунды записи
sample_rate = 44100


print("Доступные языки для перевода:")
for code, name in LANGUAGE_CODES.items():
    print(f"{code} - {name}")

lang = input("Введите код языка для перевода (например, 'en' — английский, 'es' — испанский): ")

if lang not in LANGUAGE_CODES:
    print(f"Язык '{lang}' не найден в списке поддерживаемых. Используем английский (en) по умолчанию.")
    lang = 'en'
    
print(f"Перевод будет выполнен на {LANGUAGE_CODES.get(lang, lang)}")

print("Говори...")
recording = sd.rec(
  int(duration * sample_rate), # длительность записи в сэмплах
  samplerate=sample_rate,      # частота дискретизации
  channels=1,                  # 1 — это моно
  dtype="int16")               # формат аудиоданных
sd.wait()  # ждём завершения записи


wav.write("output.wav", sample_rate, recording)
print("Запись завершена, теперь распознаём...")




recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)
    
try:
    text = recognizer.recognize_google(audio, language="ru-RU")
    print("Ты сказал:", text)

except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
    print("Не удалось распознать речь.")
except sr.RequestError as e:             # - если нет интернета или API недоступен
    print(f"Ошибка сервиса: {e}")

translated = GoogleTranslator(source="auto",target ="en").translate(text)
print("🌍Перевод на английский:", translated)
