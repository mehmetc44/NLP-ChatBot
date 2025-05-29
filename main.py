from src.gui.home import UI

ui = UI()
ui.run()
"""
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kamera Arayüzü")
        self.setMinimumSize(800, 600)

        # ComboBox tanımı
        self.combo = QComboBox()
        self.combo.addItems(["Ana Menü", "Camera Mode"])
        self.combo.currentIndexChanged.connect(self.change_mode)

        # Kamera widget'i
        self.camera_widget = CameraWidget()
        self.camera_widget.hide()

        # Beyaz ekran (ana menü görünümü)
        self.blank_label = QLabel()
        self.blank_label.setStyleSheet("background-color: white;")
        self.blank_label.setAlignment(Qt.AlignCenter)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.blank_label)
        self.layout.addWidget(self.camera_widget)
        self.setLayout(self.layout)

    def change_mode(self, index):
        if self.combo.currentText() == "Camera Mode":
            self.blank_label.hide()
            self.camera_widget.show()
            self.camera_widget.start_camera()
        else:
            self.camera_widget.stop_camera()
            self.camera_widget.hide()
            self.blank_label.show()

    def closeEvent(self, event):
        self.camera_widget.stop_camera()
        event.accept()

# Uygulama başlat
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
"""

