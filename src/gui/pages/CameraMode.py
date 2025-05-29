from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import cv2

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Kamera başlatılmaz, sadece tanımlanır
        self.cap = None

        # Kamera görüntüsünün gösterileceği QLabel
        self.label = QLabel("Kamera başlatılmadı", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black; color: white; font-size: 18px;")

        # Timer tanımı
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.blank_label = QLabel()
        self.blank_label.setStyleSheet("background-color: white;")
        self.blank_label.setAlignment(Qt.AlignCenter)


        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)




    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_camera(self):
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None
        self.label.setText("Kamera durduruldu")
        self.label.setPixmap(QPixmap())  # Boşalt

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
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

