from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, \
    QDateEdit, QComboBox, QLineEdit
from PyQt5.QtWidgets import QHeaderView
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
        main_layout.addSpacing(int(self.screen_manager.height()/4))
        self.grid = QGridLayout(self)
        self.create_calendar()

        row1 = QHBoxLayout(self)
        row1.addSpacing(int(self.screen_manager.width()/5))
        row1.addLayout(self.grid)
        row1.addSpacing(int(self.screen_manager.width()/5))

        row2 = QHBoxLayout(self)
        row2.addSpacing(int(self.screen_manager.width()/3))
        # self.date_box = QDateEdit()
        self.dropdown = QComboBox(self)
        self.amount = QLineEdit()
        self.description = QLineEdit(self)
        # row2.addWidget(self.date_box)
        row2.addWidget(self.dropdown)
        row2.addWidget(self.amount)
        row2.addWidget(self.description)
        row2.addSpacing(int(self.screen_manager.width()/3))

        row3 = QHBoxLayout(self)
        row3.addSpacing(int(self.screen_manager.width()/3))
        self.add_button = QPushButton("Add Expense", self)
        self.delete_button = QPushButton("Delete Expense", self)
        row3.addWidget(self.add_button)
        row3.addWidget(self.delete_button)
        row3.addSpacing(int(self.screen_manager.width()/3))

        row4 = QHBoxLayout(self)
        row4.addSpacing(int(self.screen_manager.width()/3))
        table_columns = 3
        table_rows = 10
        day_table = QTableWidget(table_rows, table_columns, self)
        day_table.setHorizontalHeaderLabels(["Category", "Amount", "Description"])
        day_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        row4.addWidget(day_table)
        row4.addSpacing(int(self.screen_manager.width()/3))

        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        main_layout.addLayout(row3)
        main_layout.addLayout(row4)
        self.setLayout(main_layout)

    def on_frame_click(self, frame, *args):
        for i in range(self.grid.count()):
            grid_widget = self.grid.itemAt(i).widget()
            if not isinstance(grid_widget, QLabel): # don't affect the day labels (Sun, Mon...)
                if hasattr(grid_widget, 'selected') and grid_widget.selected:
                    grid_widget.setStyleSheet("background-color: white;")
        frame.setStyleSheet("background-color: gray;")


    def create_calendar(self):
        self.calendar_boxes = []
        for i in range(31):
            frame = ClickableFrame(self)
            frame.setStyleSheet("background-color: white;")
            frame.setMaximumSize(90, 90)
            frame.setFrameShape(QFrame.StyledPanel)
            frame.clicked.connect(lambda qframe = frame: self.on_frame_click(qframe))
            frame_layout = QHBoxLayout(frame)
            day_num = QLabel(str(i), frame)
            day_num.setAlignment(Qt.AlignTop)
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
            self.grid.addWidget(day_label, 0, i)

        now = datetime.now()
        current_year = now.year
        current_month = now.month
        days_in_month = calendar.monthrange(current_year, current_month)[1]

        # Get the first day of the month (0 = Monday, 6 = Sunday)
        first_day_of_month = calendar.monthrange(current_year, current_month)[0]
        print(f"this is the first_day_of_month {first_day_of_month}")

        # Place buttons for each day of the month
        day_counter = 0
        for row in range(1, 7):
            for col in range(7):
                if row == 1 and col < first_day_of_month:
                    continue  # Skip the cells before the first day of the month
                if day_counter <= days_in_month:
                    self.grid.addWidget(self.calendar_boxes[day_counter], row, col)
                    day_counter += 1

   # def create_table(self):