from PyQt5.QtCore import QObject, QThread, pyqtSignal
import speech_recognition as sr
import time


class ContinuousSpeechWorker(QObject):
    text_detected = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    stopped = False

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        # Optimize edilmiş parametreler
        self.recognizer.pause_threshold = 0.8  # Konuşma bitişini daha hızlı algıla
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.non_speaking_duration = 0.3  # Konuşma olmayan minimum süre

    def run(self):
        with self.microphone as source:
            print("Mikrofon kalibrasyonu yapılıyor...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Dinlemeye başlandı (Konuşun...)")

            while not self.stopped:
                try:
                    # Dinleme parametreleri
                    audio = self.recognizer.listen(
                        source,
                        timeout=1.0,  # 1 saniye sessizlikte bekler
                        phrase_time_limit=5  # Maksimum 5 saniyelik konuşma
                    )

                    try:
                        text = self.recognizer.recognize_google(audio, language="tr-TR")
                        if text:  # Boş olmayan metinleri işle
                            print(f"Algılandı: {text}")
                            self.text_detected.emit(text)
                    except sr.UnknownValueError:
                        print("Ses anlaşılamadı")
                        continue
                    except sr.RequestError as e:
                        self.error_occurred.emit(f"API hatası: {e}")
                        time.sleep(2)

                except sr.WaitTimeoutError:
                    # Zaman aşımı - sessizlik durumu
                    continue
                except Exception as e:
                    self.error_occurred.emit(f"Genel hata: {e}")
                    time.sleep(1)

    def stop(self):
        self.stopped = True
        print("Dinleme durduruldu")
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
                self.finished.emit("")
            except sr.RequestError as e:
                self.error.emit(f"İstek hatası: {e}")
                self.finished.emit("")





