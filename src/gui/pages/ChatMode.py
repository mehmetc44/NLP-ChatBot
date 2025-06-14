from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLineEdit

from src.stt.SpeechToText import SpeechWorker
from utils.rasa_client import RasaClient
from utils.config import *
from src.gui.styles.colors import Colors
from PyQt5.QtCore import Qt, QThread
from src.gui.widgets.MessageBoxes import *



class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(5, 0, 5, 15)  # Dış boşluklar (sol, üst, sağ, alt)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollLayout.setAlignment(Qt.AlignTop)  # Mesajları üstte başlat
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)  # Scroll alanı ana layout'a ekleniyor
        scrollbar_style = """
        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 10px;
            margin: 0px 0px 0px 0px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background: #888;
            min-height: 20px;
            border-radius: 5px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
            subcontrol-origin: margin;
            background: none;
            border: none;
        }

        QScrollBar::add-page:vertical, 
        QScrollBar::sub-page:vertical {
            background: none;
        }
        """
        self.scrollArea.verticalScrollBar().setStyleSheet(scrollbar_style)
        self.frame_2 = QtWidgets.QFrame()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_2.setSizeIncrement(QtCore.QSize(50, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout.addWidget(self.frame_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayout.setSpacing(1)
        self.frame = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(1200, 100))
        self.frame.setSizeIncrement(QtCore.QSize(50, 50))
        self.frame.setBaseSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(1, 35, 28))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        self.frame.setPalette(palette)
        self.frame.setStyleSheet(f"background-color: {Colors.Color_Gray};\n"+
                                 "border-radius: 30px;\n"+
                                 "border: 0.5px solid rgb(100,100,100);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_2.setContentsMargins(20, 10, -1, 10)
        self.microphoneButton = QtWidgets.QPushButton(self.frame)
        self.microphoneButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.microphoneButton.setSizePolicy(sizePolicy)
        self.microphoneButton.setMinimumSize(QtCore.QSize(70, 70))
        self.microphoneButton.setSizeIncrement(QtCore.QSize(60, 60))
        self.microphoneButton.setStyleSheet("""
                    QPushButton{
                        border-radius: 30px;
                        border: none;
                        padding: 10px;
                        width: 50px;
                        image: url(data/assets/microphone-primary.svg); 
                    }
                    QPushButton:hover{
                        image: url(data/assets/microphone-secondary.svg); 
                    }
                """)
        self.microphoneButton.setText("")
        self.microphoneButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.microphoneButton, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)

        self.inputLine = QLineEdit()
        self.inputLine.setMinimumSize(QtCore.QSize(400, 60))
        self.inputLine.setStyleSheet(f"""color: white; 
                    font-size: 20px;
                    padding: 20px 10px;
                    border: 0px;
                    border-radius: 30px;
                    background-color: {Colors.Color_Dark};
                    place-holder""")
        self.inputLine.setPlaceholderText("Mesajınızı iletin...")
        self.inputLine.setObjectName("plainTextEdit")
        self.gridLayout_2.addWidget(self.inputLine, 0, 2, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.sendButton.setSizePolicy(sizePolicy)
        self.sendButton.setMinimumSize(QtCore.QSize(70, 70))
        self.sendButton.setStyleSheet("""
                    QPushButton{
                        padding: 10px;
                        width: 50px;
                        border: 0px;
                        image: url(data/assets/paper-plane-primary.svg); 
                    }
                    QPushButton:hover{
                        image: url(data/assets/paper-plane-secondary.svg); 
                    }""")
        self.sendButton.setText("")
        self.sendButton.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.sendButton, 0, 3, 1, 1)

        self.horizontalLayout.addWidget(self.frame)

        self.gridLayout.setRowStretch(0, 12)

        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.sendButton.clicked.connect(self.converse)
        self.inputLine.returnPressed.connect(self.converse)
        self.microphoneButton.clicked.connect(self.captureSpeechInput)




    def microphoneActive(self):
        self.microphoneButton.setStyleSheet("""
                    QPushButton{
                        padding: 10px;
                        width: 50px;
                        border: 0px;
                        image: url(data/assets/microphone-red.svg); 
                    }""")
    def microphoneDisactive(self):
        self.microphoneButton.setStyleSheet("""
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
        self.inputLine.setText(text)
        self.microphoneDisactive()

    def onSpeechError(self, message):
        print(message)
        self.inputLine.setText("")
        self.microphoneDisactive()


    def addMessage(self, msg_box):
        self.scrollLayout.addWidget(msg_box)
        QtCore.QTimer.singleShot(50, lambda: self.scrollArea.verticalScrollBar().setValue(
        self.scrollArea.verticalScrollBar().maximum()))

    def sendMessage(self,sender):
        text = self.inputLine.text().strip()
        if text:
            self.inputLine.clear()
            self.addMessage(MessageBox(text,sender))

    def converse(self):
        message = self.inputLine.text()
        self.inputLine.clear()
        self.addMessage(MessageBox(message,SENDER_USER))
        result = RasaClient().send_test_message()
        self.addMessage(MessageBox(result,SENDER_BOT))

