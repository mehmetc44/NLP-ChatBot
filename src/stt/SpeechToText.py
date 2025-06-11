from PyQt5.QtCore import QObject, QThread, pyqtSignal
import speech_recognition as sr
import time



class SpeechWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                try:
                    sound = r.listen(source, phrase_time_limit=8)
                    text = r.recognize_google(sound, language="en-US")  # Language changed to English
                    self.finished.emit(text)
                except sr.UnknownValueError:
                    self.error.emit("I couldn't understand.")
                    self.finished.emit("")
                except sr.RequestError as e:
                    self.error.emit(f"Request error: {e}")
                    self.finished.emit("")
        except Exception as e:
            self.error.emit(f"Microphone error: {str(e)}")
            self.finished.emit("")





