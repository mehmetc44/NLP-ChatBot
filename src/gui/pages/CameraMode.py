from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import cv2
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from src.gui.styles.colors import Colors
from src.stt.SpeechToText import SpeechWorker
from utils.rasa_client import RasaClient
import numpy as np
from multiprocessing import Process, Queue
from src.gui.pages.face_rec_3 import recognition_service


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

    def onSpeechRecognized(self, text):
        self.message_box.setText(text)
        self.microphoneDisactive()

    def onSpeechError(self, message):
        print(message)
        self.message_box.setText(message)
        self.microphoneDisactive()

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

        self.input_queue.put(None)
        self.recog_process.join()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame,1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if self.input_queue.qsize() < 2:
                self.input_queue.put(frame)

            if self.input_queue.empty():
                self.input_queue.put(frame)
            if not self.output_queue.empty():
                names = self.output_queue.get()
                if names:
                    print(f"Tanınan yüzler: {', '.join(names)}")
                else:
                    print("Yüz tespit edilemedi")

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
        message = self.inputLine.text().strip()
        if message:
            self.message_box.append(f"Kullanıcı: {message}")
            self.inputLine.clear()
            response = RasaClient().send_test_message(message)
            self.message_box.append(f"Asistan: {response}")



