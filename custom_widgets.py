from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal

class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected = None

    def mousePressEvent(self, a0):
        self.clicked.emit()
        super().mousePressEvent(a0)

    def click(self):
        self.clicked.emit()

    def random(self):
        query.prepare("SELECT json_expenses FROM answers WHERE :name=name ")