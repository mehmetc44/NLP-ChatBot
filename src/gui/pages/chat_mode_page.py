from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from src.gui.styles.colors import Colors
from src.gui.widgets.message_boxes import *

class ChatMode():
    def __init__(self,Form):
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(5, 0, 5, 15)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setStyleSheet("""margin: 5px 50px;
        margin-bottom: -20px;
        border: 0px solid white;""")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        for i in range(30):  # 30 buton ekleyelim
            button = QtWidgets.QPushButton(f"Buton {i+1}")
            button.setFixedHeight(50)  # Her butonun yüksekliği 50 piksel
            button.setStyleSheet("background-color: white;")
            self.scrollLayout.addWidget(button)
        self.scrollAreaWidgetContents.setLayout(self.scrollLayout)



        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(100, 100))
        self.frame_2.setSizeIncrement(QtCore.QSize(50, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")


        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.frame = QtWidgets.QFrame(self.frame_2)
        self.frame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(1200, 100))
        self.frame.setSizeIncrement(QtCore.QSize(50, 50))
        self.frame.setBaseSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(1, 35, 28))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        self.frame.setPalette(palette)
        self.frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame.setStyleSheet(f"background-color: {Colors.COLOR_SECONDARY};\n"
        "border-radius: 30px;\n"
        "border: 0.5px solid rgb(100,100,100);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_2.setContentsMargins(20, 10, -1, 10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        
        
        
        
        
        self.microphoneButton = QtWidgets.QPushButton(self.frame)
        self.microphoneButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.microphoneButton.sizePolicy().hasHeightForWidth())
        self.microphoneButton.setSizePolicy(sizePolicy)
        self.microphoneButton.setMinimumSize(QtCore.QSize(70, 70))
        self.microphoneButton.setSizeIncrement(QtCore.QSize(60, 60))
        self.microphoneButton.setStyleSheet("""QPushButton{
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
        self.microphoneButton.setFlat(False)
        self.microphoneButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.microphoneButton, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.frame)
        self.plainTextEdit.setMinimumSize(QtCore.QSize(400, 60))
        self.plainTextEdit.setStyleSheet(f"""color: white; 
        font-size: 20px;
        padding: 20px 10px;
        border: 0px;
        border-radius: 30px;
        background-color:{Colors.COLOR_DARK};
        place-holder""")
        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plainTextEdit.setReadOnly(False)
        self.plainTextEdit.setOverwriteMode(False)
        self.plainTextEdit.setCursorWidth(1)
        self.plainTextEdit.setBackgroundVisible(False)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_2.addWidget(self.plainTextEdit, 0, 2, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.frame)
        self.plainTextEdit.setPlaceholderText("Mesajınızı iletin...")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendButton.sizePolicy().hasHeightForWidth())
        self.sendButton.setSizePolicy(sizePolicy)
        self.sendButton.setMinimumSize(QtCore.QSize(70, 70))
        self.sendButton.setStyleSheet("""QPushButton{
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
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 12)
        print(self.scrollArea.width())
        



