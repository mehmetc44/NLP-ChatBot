class Colors:
    COLOR_LIGTH = "#d1f4fa"
    COLOR_SECONDARY = "#0078D7"

class MessageBox(QWidget):
    def __init__(self, text):
        super().__init__()
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setText(text)
        self.textEdit.setWordWrapMode(QtGui.QTextOption.WordWrap)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.adjustTextEditSize()

    def adjustTextEditSize(self):
        doc = self.textEdit.document()
        doc.setTextWidth(330)
        height = doc.size().height() + 20
        self.textEdit.setFixedHeight(int(height))
        self.setFixedHeight(int(height + 20))

class SendMessageBox(MessageBox):
    def __init__(self, text):
        super().__init__(text)
        self.textEdit.setStyleSheet("background-color: lightblue; padding: 10px; border-radius: 15px;")
        self.layout.addStretch()
        self.layout.addWidget(self.textEdit)

class ReceiveMessageBox(MessageBox):
    def __init__(self, text):
        super().__init__(text)
        self.horizontalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addItem(self.spacerItem)

        self.textEdit.setStyleSheet(f"""
            background-color: {Colors.COLOR_SECONDARY};
            color: white;
            border-radius: 20px;
            border: 1px solid black;
            padding: 10px 20px;
            font-size: 16px;
        """)

        self.setMessage(text)