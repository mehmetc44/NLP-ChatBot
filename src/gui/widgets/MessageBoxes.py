from PyQt5 import QtWidgets, QtCore, QtGui
from src.gui.styles.colors import Colors

class MessageBox(QtWidgets.QWidget):
    def __init__(self, text, sender):
        super().__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(10)

        self.label = QtWidgets.QLabel()
        self.label.setText(text)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.setStyleSheet("font-size: 20px;")

        self._min_width = 200
        self._min_height = 60
        self.setMinimumSize(self._min_width, self._min_height)

        QtCore.QTimer.singleShot(0, lambda: self.adjustLabelSize(parent_width=self.width()))
        self.setMessage(text)
        if(sender == "User"):
            self.horizontalLayout.addItem(self.spacerItem)
            self.horizontalLayout.addWidget(self.label)
            self.label.setStyleSheet(f"""
                    background-color: {Colors.Color_Gray};
                    color: white;
                    border-radius: 15px;
                    border: 1px solid black;
                    padding: 10px;
                """)
        elif(sender=="Bot"):
            self.horizontalLayout.addWidget(self.label)
            self.horizontalLayout.addItem(self.spacerItem)

            self.label.setStyleSheet(f"""
                        background-color: {Colors.Color_Light};
                        color: black;
                        border-radius: 15px;
                        border: 1px solid black;
                        padding: 10px;
                    """)

    def setMessage(self, message):
        self.label.setText(message)
        self.adjustLabelSize()

    def adjustLabelSize(self, max_width=None, parent_width=None):
        effective_parent_width = parent_width if parent_width is not None else self.width()
        margin = 120 if effective_parent_width > 400 else 60

        calculated_max_width = max(self._min_width, effective_parent_width - margin)
        max_width = calculated_max_width if max_width is None else min(max_width, calculated_max_width)

        font_metrics = QtGui.QFontMetrics(self.label.font())
        text_width = font_metrics.horizontalAdvance(self.label.text()) + 60

        if max_width:
            self.label.setMaximumWidth(min(text_width, max_width) if text_width < 300 else max_width)
        else:
            self.label.setMaximumWidth(16777215)
        doc = QtGui.QTextDocument()
        doc.setDefaultFont(self.label.font())
        doc.setPlainText(self.label.text())
        doc.setTextWidth(self.label.width() - 30)
        self.setFixedHeight(max(int(doc.size().height() + 40), self._min_height))


    def updateMaxWidth(self, parent_width):
        max_width = max(200, parent_width)
        self.adjustLabelSize(max_width)

    def resizeEvent(self, event):
        self.updateMaxWidth(event.size().width())
        super().resizeEvent(event)










