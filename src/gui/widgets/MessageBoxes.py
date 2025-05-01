
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QSpacerItem, QSizePolicy, QApplication, QMainWindow
import sys
from src.gui.styles.colors import Colors

class MessageBox(QtWidgets.QWidget):
    def __init__(self, text):
        super().__init__()

        # Main layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(10)

        # Label setup
        self.label = QtWidgets.QLabel()
        self.label.setText(text)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        # Spacer
        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.setStyleSheet("font-size: 20px;")
        self.setMessage(text)

    def setMessage(self, message):
        self.label.setText(message)
        self.adjustLabelSize()

    def adjustLabelSize(self, max_width=None, parent_width=None):
        # Eğer parent_width verilmişse, max_width'yi hesapla
        if parent_width is not None:
            margin = 120  # Total side margins
            max_width = max(200, parent_width - margin)

        if max_width:
            # Metnin gerçek genişliğini hesapla
            font_metrics = QtGui.QFontMetrics(self.label.font())
            text_width = font_metrics.horizontalAdvance(self.label.text()) + 60  # Padding dahil

            # Kısa mesajlar için optimize
            if text_width < 300:
                self.label.setMaximumWidth(text_width)
            else:
                self.label.setMaximumWidth(max_width)
        else:
            self.label.setMaximumWidth(16777215)  # Qt'nin maksimum değeri

        # Orijinal yükseklik hesaplama
        self.label.adjustSize()
        doc = QtGui.QTextDocument()
        doc.setDefaultFont(self.label.font())
        doc.setPlainText(self.label.text())
        doc.setTextWidth(self.label.width() - 30)
        height = doc.size().height() + 40
        min_height = 60
        self.setFixedHeight(max(int(height), min_height))

    def updateMaxWidth(self, parent_width):
        margin = 120  # Total side margins
        max_width = max(200, parent_width - margin)
        self.adjustLabelSize(max_width)

    def resizeEvent(self, event):
        self.updateMaxWidth(event.size().width())
        super().resizeEvent(event)
class SendMessageBox(MessageBox):
    def __init__(self, text):
        super().__init__(text)
        self.horizontalLayout.addItem(self.spacerItem)
        self.horizontalLayout.addWidget(self.label)

        self.label.setStyleSheet(f"""
            background-color: {Colors.Color_Gray};
            color: white;
            border-radius: 15px;
            border: 1px solid black;
            padding: 10px;
        """)


class ReceiveMessageBox(MessageBox):
    def __init__(self, text):
        super().__init__(text)
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addItem(self.spacerItem)

        self.label.setStyleSheet(f"""
            background-color: {Colors.Color_Light};
            color: black;
            border-radius: 15px;
            border: 1px solid black;
            padding: 10px;
        """)







