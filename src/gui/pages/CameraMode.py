from PyQt5.QtCore import QTimer, QSize, QObject, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import cv2
from PyQt5.QtCore import QThread
from src.gui.styles.colors import Colors
from src.stt.SpeechToText import SpeechWorker
import numpy as np
from multiprocessing import Process, Queue
from src.vision.FaceRecognition import recognition_service
from src.vision.HandDetection import HandGestureRecognizer
from queue import Full, Empty
from utils.rasa_client import RasaClient
import src.tts.TextToSpeech as tts
from src.tts.TextToSpeech import TextToSpeechWorker



class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cap = None

        self.camera_mode_active = False
        self.hand_gesture = HandGestureRecognizer()

        # Kamera görüntüsü için QLabel
        self.label = QLabel("Kamera başlatılmadı", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black; color: white; font-size: 18px;")

        # Mesaj kutusu (konuşma tanıma sonuçları için)
        self.message_box = QTextEdit()
        self.message_box.setReadOnly(True)
        self.message_box.setMaximumHeight(100)
        self.message_box.setStyleSheet(f"""color: white; 
                    font-size: 18px;
                    padding: 5px 10px;
                    border: 0px;
                    border-radius: 30px;
                    background-color: {Colors.Color_Gray};
                    place-holder""")

        # Mikrofon butonu
        self.mic_button = QPushButton()
        self.mic_button.setIcon(QIcon.fromTheme("microphone"))
        self.mic_button.setIconSize(QSize(32, 32))
        self.mic_button.setFixedSize(60, 60)
        self.mic_button.setStyleSheet("""
                    QPushButton{
                        padding: 10px;
                        width: 50px;
                        border: 0px;
                        image: url(data/assets/microphone-primary.svg); 
                    }
                    QPushButton:hover{
                        image: url(data/assets/microphone-secondary.svg); 
                    }
                """)

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

        self.input_queue = Queue()
        self.output_queue = Queue()
        self.recog_process = Process(target=recognition_service, args=(self.input_queue, self.output_queue))
        self.recog_process.start()


        self.mic_button.clicked.connect(self.captureSpeechInput)
    def update_frame(self):
        if self.camera_mode_active and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                frame = self.get_empty_frame()
        else:
            frame = self.get_empty_frame()

        # Parmak ve jest algılama
        frame, finger_count, gesture = self.hand_gesture.process_frame(frame)

        text = f"Fingers: {finger_count}"
        if gesture:
            text += f" | Gesture: {gesture}"

        cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2)

        # input_queue'ya frame gönder
        try:
            if self.input_queue.qsize() < 2:  # Kuyruk doluysa ekleme
                self.input_queue.put_nowait(frame)
        except Full:
            pass

        # output_queue'dan yüz tanıma sonuçlarını al
        try:
            names = self.output_queue.get_nowait()
            if names:
                print(f"Tanınan yüzler: {', '.join(names)}")
            else:
                print("Yüz tespit edilemedi")
        except Empty:
            pass

        # Frame'i GUI'ye yansıt
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        scaled_img = img.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(QPixmap.fromImage(scaled_img))

    def get_empty_frame(self, width=640, height=480, channels=3):
        # Siyah, boş frame üretir
        return np.zeros((height, width, channels), dtype=np.uint8)



    def microphoneActive(self):
        self.mic_button.setStyleSheet("""
                        QPushButton{
                            padding: 10px;
                            width: 50px;
                            border: 0px;
                            image: url(data/assets/microphone-red.svg); 
                        }""")

    def microphoneDisactive(self):
        self.mic_button.setStyleSheet("""
                                QPushButton{
                                    padding: 10px;
                                    width: 50px;
                                    border: 0px;
                                    image: url(data/assets/microphone-primary.svg); 
                                }
                                QPushButton:hover{
                                    image: url(data/assets/microphone-secondary.svg); 
                                }""")

    def captureSpeechInput(self):
        self.microphoneActive()
        self.thread = QThread()
        self.worker = SpeechWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.onSpeechRecognized)
        self.worker.error.connect(self.onSpeechError)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def onRasaResponse(self, response):
        # Şimdi cevabı seslendir
        self.tts_thread = QThread()
        self.tts_worker = tts.TextToSpeechWorker(response)
        self.tts_worker.moveToThread(self.tts_thread)

        self.tts_thread.started.connect(self.tts_worker.run)
        self.tts_worker.finished.connect(self.tts_thread.quit)
        self.tts_worker.finished.connect(self.tts_worker.deleteLater)
        self.tts_thread.finished.connect(self.tts_thread.deleteLater)

        self.tts_thread.start()

    def onSpeechRecognized(self, text):
        self.message_box.setText(text)
        self.microphoneDisactive()

        # Rasa'ya mesajı gönder ve cevap al (thread içinde)
        self.rasa_thread = QThread()
        self.rasa_worker = RasaWorker(text)
        self.rasa_worker.moveToThread(self.rasa_thread)

        self.rasa_thread.started.connect(self.rasa_worker.run)
        self.rasa_worker.finished.connect(self.onRasaResponse)
        self.rasa_worker.finished.connect(self.rasa_thread.quit)
        self.rasa_worker.finished.connect(self.rasa_worker.deleteLater)
        self.rasa_thread.finished.connect(self.rasa_thread.deleteLater)

        self.rasa_thread.start()

    def onSpeechError(self, message):
        print(message)
        self.microphoneDisactive()

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        self.camera_mode_active = True
        self.timer.start(30)

    def stop_camera(self):
        self.camera_mode_active = False
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None
        self.label.setText("Camera stopped")
        self.label.setPixmap(QPixmap())


    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.cap and self.label.pixmap():
            self.update_frame()

    def closeEvent(self, event):
        print("[INFO] Closing CameraWidget, terminating face recognition process.")

        if self.cap:
            self.stop_camera()

        if hasattr(self, 'recog_process') and self.recog_process.is_alive():
            try:
                self.input_queue.put(None)  # Temiz çıkış sinyali
                self.recog_process.join(timeout=3)
                if self.recog_process.is_alive():
                    print("[WARN] Process still alive. Forcing termination.")
                    self.recog_process.terminate()
            except Exception as e:
                print(f"[ERROR] during shutdown: {e}")

        event.accept()

class RasaWorker(QObject):
    finished = pyqtSignal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        response = RasaClient().send_test_message()
        self.finished.emit(response)


