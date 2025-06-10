from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import cv2
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from src.stt.SpeechToText import ContinuousSpeechWorker
from src.tts import TextToSpeech as tts
from utils.rasa_client import RasaClient


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cap = None

        # Kamera görüntüsü için QLabel
        self.label = QLabel("Kamera başlatılmadı", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black; color: white; font-size: 18px;")

        # Mesaj kutusu (konuşma tanıma sonuçları için)
        self.message_box = QTextEdit()
        self.message_box.setReadOnly(True)
        self.message_box.setMaximumHeight(100)
        self.message_box.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px;
                font-size: 14px;
            }
        """)

        # Mikrofon butonu
        self.mic_button = QPushButton()
        self.mic_button.setIcon(QIcon.fromTheme("microphone"))
        self.mic_button.setIconSize(QSize(32, 32))
        self.mic_button.setFixedSize(60, 60)
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border-radius: 30px;
                border: 2px solid #a0a0a0;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
        """)
        self.mic_button.clicked.connect(self.toggle_microphone)

        # Buton ve mesaj kutusu için yatay layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.mic_button)
        bottom_layout.addWidget(self.message_box)
        bottom_layout.setSpacing(10)

        # Ana layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(bottom_layout)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.listening = False
        self.speech_thread = None
        self.speech_worker = None

    def toggle_microphone(self):
        self.listening = not self.listening

        if self.listening:
            self.mic_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff4444;
                    border-radius: 30px;
                    border: 2px solid #cc0000;
                }
            """)
            self.start_speech_recognition()
            self.message_box.append("Dinleme başladı...")
        else:
            self.mic_button.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    border-radius: 30px;
                    border: 2px solid #a0a0a0;
                }
            """)
            self.stop_speech_recognition()
            self.message_box.append("Dinleme durduruldu")


    def on_error_occurred(self, error):
        self.message_box.append(f"Hata: {error}")
        self.tts_worker = TTSWorker(error)
        self.tts_thread = QThread()
        self.tts_worker.moveToThread(self.tts_thread)
        self.tts_thread.started.connect(self.tts_worker.run)
        self.tts_worker.finished.connect(self.tts_thread.quit)
        self.tts_worker.finished.connect(self.tts_worker.deleteLater)
        self.tts_thread.finished.connect(self.tts_thread.deleteLater)
        self.tts_worker.error_occurred.connect(lambda e: print(f"TTS Error: {e}"))
        self.tts_thread.start()
    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        self.timer.start(30)
    def stop_camera(self):
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None
        self.label.setText("Camera stopped")
        self.label.setPixmap(QPixmap())
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame,1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            scaled_img = img.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(QPixmap.fromImage(scaled_img))
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.cap and self.label.pixmap():
            self.update_frame()
    def converse(self):
        pass

        message = self.inputLine.text()
        self.inputLine.clear()
        result = RasaClient().send_test_message()
    def on_text_detected(self, text):
        self.message_box.append(f"Algılandı: {text}")
        #result = RasaClient().send_test_message()
        #self.converse(result)


class TTSWorker(QObject):
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    def __init__(self, error_message):
        super().__init__()
        self.error_message = error_message

    def run(self):
        try:
            tts.speak(self.error_message)  # TTS işlemi
        except Exception as e:
            self.error_occurred.emit(str(e))  # Hata sinyali
        finally:
            self.finished.emit()  # İşlem tamamlandı

