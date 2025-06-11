from gtts import gTTS
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import os
import random
import ctypes  # BURAYA DİKKAT


def playaudio(file_path):
    alias = "mp3audio"
    file_path = os.path.abspath(file_path).replace("/", "\\")  # Güvenli hale getir
    open_cmd = f'open "{file_path}" type mpegvideo alias {alias}'
    play_cmd = f'play {alias} wait'
    close_cmd = f'close {alias}'

    ctypes.windll.winmm.mciSendStringW(open_cmd, None, 0, None)
    ctypes.windll.winmm.mciSendStringW(play_cmd, None, 0, None)
    ctypes.windll.winmm.mciSendStringW(close_cmd, None, 0, None)


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


class TextToSpeechWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text

    @pyqtSlot()
    def run(self):
        speak(self.text)
        self.finished.emit()
