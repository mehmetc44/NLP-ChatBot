from PyQt5.QtCore import QObject, QThread, pyqtSignal
import speech_recognition as sr

class SpeechWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            try:
                sound = r.listen(source, phrase_time_limit=8)
                text = r.recognize_google(sound, language="tr")
                self.finished.emit(text)
            except sr.UnknownValueError:
                self.error.emit("Anlayamadım.")
            except sr.RequestError as e:
                self.error.emit(f"İstek hatası: {e}")






