from gtts import gTTS
from PyQt5.QtCore import QObject, pyqtSignal
import os
import random
from playaudio import playaudio

def speak(text):
    text = text.lower()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    audio_dir = os.path.join(base_dir, "data", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    file_path = os.path.join(audio_dir, f"audio{random.randint(1, 9999999)}.mp3")
    try:
        tts = gTTS(text=text, lang="tr", slow=False)
        tts.save(file_path)
        playaudio(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


from src.tts import TextToSpeech as tts

class TextToSpeechWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        tts.speak(self.text)
        self.finished.emit()
