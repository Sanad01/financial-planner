from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont
import calendar
from datetime import datetime

from data.database import DatabaseManager
from custom_widgets import ClickableFrame


class HomeScreen(QWidget):

    def __init__(self, screen_manager):
        super().__init__()
        self.db = DatabaseManager()
        self.screen_manager = screen_manager

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        row1 = QHBoxLayout(self)
        grid = QGridLayout(self)

        self.calendar_boxes = []
        for i in range(31):
            frame = QFrame(self)
            frame.setStyleSheet("background-color: white;")
            frame.setMaximumSize(90, 90)
            frame_layout = QHBoxLayout(frame)
            day_num = QLabel(str(i), frame)
            day_num.setAlignment(Qt.AlignTop)
            frame.setFrameShape(QFrame.StyledPanel)
            frame_layout.addWidget(day_num)
            self.calendar_boxes.append(frame)

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sunday']
        # font for day labels
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)

        # create a label for each day
        for i, day in enumerate(days):
            day_label = QLabel(day, self)
            day_label.setFont(font)
            day_label.setMaximumHeight(50)
            day_label.setStyleSheet("background-color: #bf0404;"
                                    "border: 1px solid white;")
            day_label.setFrameShape(QFrame.Panel)
            day_label.setFrameShadow(QFrame.Raised)
            day_label.setAlignment(Qt.AlignCenter)
            day_label.resize(self.calendar_boxes[1].width(), self.calendar_boxes[1].height())
            grid.addWidget(day_label, 0, i)  # row 0, column i

        now = datetime.now()
        current_year = now.year
        current_month = now.month
        days_in_month = calendar.monthrange(current_year, current_month)[1]

        # Get the first day of the month (0 = Monday, 6 = Sunday)
        first_day_of_month = calendar.monthrange(current_year, current_month)[0]
        print(f"this is the first_day_of_month {first_day_of_month}")

        # Place buttons for each day of the month
        day_counter = 0
        for row in range(1, 7):  # Up to 6 weeks in a month
            for col in range(7):  # 7 days in a week
                if row == 1 and col < first_day_of_month:
                    continue  # Skip the cells before the first day of the month
                if day_counter <= days_in_month:
                    grid.addWidget(self.calendar_boxes[day_counter], row, col)
                    day_counter += 1

        row1.addSpacing(int(self.screen_manager.width()/5))
        row1.addLayout(grid)
        row1.addSpacing(int(self.screen_manager.width()/5))
        main_layout.addLayout(row1)
        self.setLayout(main_layout)

        def on_frame_click

    # def calendar_box(self, box):