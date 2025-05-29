from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QVBoxLayout

from src.gui.pages.ChatMode import ChatWidget
from src.gui.pages.CameraMode import CameraWidget
from src.gui.widgets.MessageBoxes import *
from src.gui.styles.colors import Colors
import src.stt.SpeechToText as stt
from src.stt.SpeechToText import SpeechWorker

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet(f"background-color: {Colors.Color_MidDark};")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setStyleSheet(f"background-color: {Colors.Color_MidDark};")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setStyleSheet(f"background-color: {Colors.Color_MidDark};")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")


        self.comboBox = QtWidgets.QComboBox(self.frame_3)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 201, 41))
        self.comboBox.setStyleSheet(f""" QComboBox{{
                border: 2px solid white;
              border-radius: 15px; 
                padding: 5px 0px 10px 5px;
                font-size: 14px;
                color: white;
                background-color: {Colors.Color_Dark};
                font: 75 12pt \"Nirmala UI\";
            }}
            QComboBox QAbstractItemView {{
                selection-background-color: #004c47;
                color: white;
                selection-color: white;
                border-radius: 10px;
               padding: 5px;
            }}
            QComboBox::down-arrow {{
               image: url(data/assets/chevron-down-white.svg); 
                width: 14px;
                height: 14px;
            }}
            QComboBox::drop-down {{
                border: none;
               width: 30px;
            }}""")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Chat Mode")
        self.comboBox.addItem("Camera Mode")
        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 1)
        self.gridLayout.setRowMinimumHeight(0, 75)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 10)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # Ana layout: Tüm bileşenleri tutan grid layout
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setContentsMargins(5, 0, 5, 15)  # Dış boşluklar (sol, üst, sağ, alt)
        self.gridLayout.setObjectName("gridLayout")

        self.camera_widget = CameraWidget()
        self.camera_widget.hide()
        self.chatMode = ChatWidget()
        self.gridLayout.addWidget(self.camera_widget)
        self.gridLayout.addWidget(self.chatMode)
        self.chatMode.microphoneButton.clicked.connect(self.captureSpeechInput)
        self.comboBox.currentIndexChanged.connect(self.change_mode)

    def change_mode(self, index):
        if self.comboBox.currentText() == "Camera Mode":
            self.chatMode.hide()
            self.camera_widget.show()
            self.camera_widget.start_camera()
        else:
            self.camera_widget.stop_camera()
            self.camera_widget.hide()
            self.chatMode.show()

    def closeEvent(self, event):
        self.camera_widget.stop_camera()
        event.accept()


    def microphoneActive(self):
        self.chatMode.microphoneButton.setStyleSheet("""
                    QPushButton{
                        padding: 10px;
                        width: 50px;
                        border: 0px;
                        image: url(data/assets/microphone-red.svg); 
                    }""")
    def microphoneDisactive(self):
        self.chatMode.microphoneButton.setStyleSheet("""
                            QPushButton{
                                padding: 10px;
                                width: 50px;
                                border: 0px;
                                image: url(data/assets/microphone-primary.svg); 
                            }
                            QPushButton:hover{
                                image: url(data/assets/microphone-secondary.svg); 
                            }""")
    def toText(self):
        text = stt.toText()
        self.chatMode.inputLine.setText("")
        self.chatMode.inputLine.setText(text)

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
        self.chatMode.inputLine.setText(text)
        self.microphoneDisactive()

    def onSpeechError(self, message):
        print(message)
        self.chatMode.inputLine.setText("")
        self.microphoneDisactive()


class UI:
    def __init__(self):
        self.UI_MainWindow = Ui_MainWindow()
    def run(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.UI_MainWindow.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())


    
