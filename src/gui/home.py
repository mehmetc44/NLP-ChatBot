from PyQt5 import QtCore, QtWidgets

from src.gui.pages.chat_mode_page import ChatMode
from src.gui.widgets.message_boxes import *

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
        self.frame.setStyleSheet("background-color: black;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setStyleSheet("background-color: blue;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setStyleSheet("background-color: #013220;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.chatMode = ChatMode(self.frame_2)


        self.comboBox = QtWidgets.QComboBox(self.frame_3)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 201, 41))
        self.comboBox.setStyleSheet(""" QComboBox {
                border: 2px solid white;
              border-radius: 15px; 
                padding: 5px 0px 10px 5px;
                font-size: 14px;
                color: white;
                background-color: #013220;
                font: 75 12pt \"Nirmala UI\";
            }
            QComboBox QAbstractItemView {
                selection-background-color: #004c47;
                color: white;
                selection-color: white;
                border-radius: 10px;
               padding: 5px;
            }
            QComboBox::down-arrow {
               image: url(data/assets/chevron-down-white.svg); 
                width: 14px;
                height: 14px;
            }
            QComboBox::drop-down {
                border: none;
               width: 30px;
            }""")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("CHAT MODE")
        self.comboBox.addItem("VIDEO MODE")
        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 1)
        self.gridLayout.setRowMinimumHeight(0, 75)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 10)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        

        QtCore.QMetaObject.connectSlotsByName(MainWindow)



        self.addMessageButton = self.chatMode.sendButton
        self.addMessageButton.clicked.connect(lambda: self.addMessageBox(self.chatMode.plainTextEdit.toPlainText())) 

    def addMessageBox(self,text):
        messageBox = SendMessageBox(text)
        self.chatMode.scrollLayout.addWidget(messageBox.frame)

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


    
