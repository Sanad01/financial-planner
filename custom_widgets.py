from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal

class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected = False

    def mousePressEvent(self, a0):
        self.clicked.emit()
        self.selected = True
        self.setStyleSheet("background-color: red;")
        super().mousePressEvent(a0)