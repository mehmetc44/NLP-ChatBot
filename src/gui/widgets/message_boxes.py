
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QFrame
from src.gui.styles.colors import Colors

class MessageBox(QWidget):
    def __init__(self,text):
        super().__init__()
        self.label = QtWidgets.QLabel()
        self.label.setText(text)
        self.label.setWordWrap(True)
        self.textEdit.setObjectName("label")
        
        self.textEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        

    def setMessage(self, message):
        self.textEdit.setPlainText(message)
        self.adjustTextEditSize()
        self.frame.setFixedHeight(self.textEdit.height()+40)
    def adjustTextEditSize(self):
        document = self.textEdit.document()
        font_metrics = QtGui.QFontMetrics(self.textEdit.font())
        
        text_width = font_metrics.width(self.textEdit.toPlainText())

        new_width = 0
        if text_width<330:
            new_width=text_width*(600/330)
        else:
            new_width=600
        total_height=0
        if new_width/500>1:
            total_height=(int((text_width)/330)+1)*40
        else:
            total_height =  40


        self.textEdit.setFixedHeight(int(total_height)+100)

class SendMessageBox(MessageBox):
    def __init__(self,text):
        super().__init__()
        self.horizontalLayout.addItem(self.spacerItem)
        self.horizontalLayout.addWidget(self.textEdit)
        self.textEdit.setStyleSheet(f"background-color: {Colors.COLOR_LIGTH}ff1;\n"
                                    "border-radius: 20px;\n"
                                    "border: 1px solid black;\n"
                                    "padding: 10px 20px;\n"
                                    "font-size: 20px;")
        self.setMessage(text)

class ReceiveMessageBox(MessageBox):
    def __init__(self,text):
        super().__init__()
        self.horizontalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addItem(self.spacerItem)
        self.textEdit.setStyleSheet(f"background-color: {Colors.COLOR_SECONDARY};\n"
                                    "border-radius: 20px;\n"
                                    "border: 1px solid black;\n"
                                    "color: white;\n"
                                    "padding: 10px 20px;\n"
                                    "font-size: 20px;")
        self.setMessage(text)
        



