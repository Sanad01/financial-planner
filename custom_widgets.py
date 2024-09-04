from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal

class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)