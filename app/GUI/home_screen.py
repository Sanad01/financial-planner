from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
import calendar
from datetime import datetime

from data.database import DatabaseManager


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

            frame_layout = QHBoxLayout(frame)
            day_num = QLabel(str(i), frame)

            frame.setFrameShape(QFrame.StyledPanel)
            frame_layout.addWidget(day_num)
            self.calendar_boxes.append(frame)


        # Example of placing days of the week at the top
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sunday']
        for i, day in enumerate(days):
            label = QLabel(day)
            label.resize(self.calendar_boxes[1].width(), self.calendar_boxes[1].height())
        
            grid.addWidget(label, 0, i)  # row 0, column i

        now = datetime.now()
        current_year = now.year
        current_month = now.month

        # Example of placing buttons for each day
        days_in_month = calendar.monthrange(current_year, current_month)[1]

        # Get the first day of the month (0 = Monday, 6 = Sunday)
        first_day_of_month = calendar.monthrange(current_year, current_month)[0]
        print(f"this is the first_day_of_month {first_day_of_month}")

        # Place buttons for each day of the month
        day_counter = 1
        for row in range(1, 7):  # Up to 6 weeks in a month
            for col in range(7):  # 7 days in a week
                if row == 1 and col < first_day_of_month:
                    continue  # Skip the cells before the first day of the month
                if day_counter <= days_in_month:
                    grid.addWidget(self.calendar_boxes[day_counter - 1], row, col)
                    day_counter += 1

        row1.addSpacing(int(self.screen_manager.width()/5))
        row1.addLayout(grid)
        row1.addSpacing(int(self.screen_manager.width()/5))
        main_layout.addLayout(row1)
        self.setLayout(main_layout)


    # def calendar_box(self, box):