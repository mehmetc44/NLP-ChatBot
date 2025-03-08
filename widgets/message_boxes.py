
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QFrame
from styles.colors import Colors

class MessageBox():
    def __init__(self,Frame):

        self.frame = QtWidgets.QFrame(Frame)
        self.frame.setStyleSheet("background-color: #013220;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)


        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.textEdit.setReadOnly(True)  # Kullanıcı düzenleyemesin
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
        print(text_width)
        if text_width<330:
            new_width=text_width*(600/330)
        else:
            new_width=600
        total_height=0
        print(new_width)
        if new_width/500>1:
            total_height=(int((text_width)/330)+1)*40
        else:
            total_height =  40

        self.textEdit.setFixedWidth(int(new_width))
        self.textEdit.setFixedHeight(int(total_height))
        print(self.textEdit.width())

class SendMessageBox(MessageBox):
    def __init__(self,Frame):
        super().__init__(Frame)
        self.horizontalLayout.addItem(self.spacerItem)
        self.horizontalLayout.addWidget(self.textEdit)
        self.textEdit.setStyleSheet(f"background-color: {Colors.COLOR_LIGTH}ff1;\n"
                                    "border-radius: 20px;\n"
                                    "border: 1px solid black;\n"
                                    "padding: 10px 20px;\n"
                                    "font-size: 20px;")

class ReceiveMessageBox(MessageBox):
    def __init__(self,Frame):
        super().__init__(Frame)
        self.horizontalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addItem(self.spacerItem)
        self.textEdit.setStyleSheet(f"background-color: {Colors.COLOR_SECONDARY};\n"
                                    "border-radius: 20px;\n"
                                    "border: 1px solid black;\n"
                                    "color: white;\n"
                                    "padding: 10px 20px;\n"
                                    "font-size: 20px;")
        




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = ReceiveMessageBox(Frame)
    ui.setMessage("M sakın iyom sakın Usmanım seni i seviyom seviyomm muşlu yar Usmanım seni i seviyom seviyomm muşlu yar Usmanım seni i seviyom seviyomm muşlu yar")
    Frame.show()
    sys.exit(app.exec_())
