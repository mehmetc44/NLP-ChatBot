from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QPushButton, QLineEdit, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QColor

from PyQt5.QtCore import QSize, Qt, QRectF
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import QLabel, QSizePolicy


class ChatBubble(QLabel):
    def __init__(self, text, is_user, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.setWordWrap(True)
        self.setMargin(12)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setText(text)

        # Responsive boyutlandırma politikaları
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.setMinimumWidth(50)
        self.setMaximumWidth(500)  # Maksimum genişlik sınırı

        # Dinamik minimum yükseklik
        self.setMinimumHeight(30)

        # Metin rengi ve arkaplan
        self.bg_color = QColor("#DCF8C6" if is_user else "#FFFFFF")
        self.text_color = QColor("#000000")

    def sizeHint(self):
        # Metin boyutuna göre uygun boyut önerisi
        fm = self.fontMetrics()
        text_width = fm.width(self.text())
        text_height = fm.height() * (self.text().count('\n') + 1)

        # Ekran genişliğinin %70'ini geçmeyecek şekilde ayarla
        max_width = min(self.parent().width() * 0.7, self.maximumWidth())
        width = min(text_width + 40, max_width)
        height = max(text_height + 20, self.minimumHeight())

        return QSize(width, height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Balon path'i oluştur
        path = QPainterPath()
        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        radius = 10

        # Balon şekli
        path.addRoundedRect(rect, radius, radius)

        # Balon kuyruğu
        if self.is_user:
            tail = QPainterPath()
            tail.moveTo(rect.right() - 5, rect.bottom())
            tail.lineTo(rect.right() + 5, rect.bottom() - 10)
            tail.lineTo(rect.right() - 5, rect.bottom() - 5)
            path.addPath(tail)
        else:
            tail = QPainterPath()
            tail.moveTo(rect.left() + 5, rect.bottom())
            tail.lineTo(rect.left() - 5, rect.bottom() - 10)
            tail.lineTo(rect.left() + 5, rect.bottom() - 5)
            path.addPath(tail)

        # Dolgu ve kenarlık
        painter.fillPath(path, self.bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        # Metin alanı (kenar boşlukları dahil)
        text_rect = rect.toRect().adjusted(10, 5, -10, -5)
        painter.setPen(self.text_color)
        painter.drawText(text_rect, Qt.AlignLeft | Qt.TextWordWrap, self.text())


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Responsive WhatsApp Clone')
        self.setMinimumSize(300, 500)

        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # Mesajlar için scroll alanı (responsive olarak genişlesin)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(5)
        self.chat_layout.setContentsMargins(5, 5, 5, 5)
        self.chat_container.setLayout(self.chat_layout)

        self.scroll_area.setWidget(self.chat_container)
        main_layout.addWidget(self.scroll_area)

        # Mesaj giriş alanı (alt kısımda sabit)
        input_layout = QHBoxLayout()
        input_layout.setSpacing(5)

        self.message_input = QLineEdit()
        self.message_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.send_button = QPushButton("Gönder")
        self.send_button.setFixedWidth(80)
        self.send_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

        # Pencere boyutu değiştiğinde mesajları yeniden boyutlandır
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.update_bubbles)
        self.resizeEvent = self.on_resize

    def on_resize(self, event):
        self.resize_timer.start(100)
        super().resizeEvent(event)

    def update_bubbles(self):
        # Tüm mesaj balonlarını güncelle
        for i in range(self.chat_layout.count()):
            container = self.chat_layout.itemAt(i).widget()
            if container:
                bubble = container.findChild(ChatBubble)
                if bubble:
                    bubble.updateGeometry()

        # Scroll'u en alta getir
        QTimer.singleShot(50, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def send_message(self):
        message = self.message_input.text()
        if message:
            self.message_input.clear()
            processor = MessageProcessor(message, True)
            processor.message_processed.connect(self.add_message)
            processor.start()

    def add_message(self, text, is_user):
        bubble = ChatBubble(text, is_user)

        # Mesajı sağa veya sola hizala
        message_layout = QHBoxLayout()
        message_layout.setContentsMargins(0, 0, 0, 0)
        message_layout.setSpacing(0)

        if is_user:
            message_layout.addStretch(1)
            message_layout.addWidget(bubble)
        else:
            message_layout.addWidget(bubble)
            message_layout.addStretch(1)

        # Layout'u bir container widget'a ekle
        container = QWidget()
        container.setLayout(message_layout)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chat_layout.addWidget(container)

        # Scroll'u en alta getir
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        # Scroll alanını en alta indir
        scroll_bar = self.scroll_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        # Eğer hemen çalışmazsa bir süre sonra tekrar dene
        QTimer.singleShot(100, lambda: scroll_bar.setValue(scroll_bar.maximum()))


class MessageProcessor(QThread):
    message_processed = pyqtSignal(str, bool)

    def __init__(self, text, is_user):
        super().__init__()
        self.text = text
        self.is_user = is_user

    def run(self):
        # Uzun mesaj işlemleri burada
        processed_text = self.text  # Gerekirse işlem yap
        self.message_processed.emit(processed_text, self.is_user)
if __name__ == '__main__':
    app = QApplication([])
    window = ChatWindow()
    window.show()
    app.exec_()