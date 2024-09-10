from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, \
    QDateEdit, QComboBox, QLineEdit, QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QFont, QIntValidator
import calendar
from datetime import datetime

from data.database import DatabaseManager
from custom_widgets import ClickableFrame
from app.GUI.fonts import table_style


class HomeScreen(QWidget):

    def __init__(self, screen_manager):
        super().__init__()
        self.db = DatabaseManager()
        self.screen_manager = screen_manager
        self.data = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: []
        }
        self.tables = []
        print(self.data)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.addSpacing(int(self.screen_manager.height()/13))
        self.grid = QGridLayout(self)
        self.create_calendar()


        # first row
        row1 = QHBoxLayout(self)
        row1.addSpacing(int(self.screen_manager.width()/5))
        row1.addLayout(self.grid)
        row1.addSpacing(int(self.screen_manager.width()/5))

        # second row
        row2 = QHBoxLayout(self)
        row2.addSpacing(int(self.screen_manager.width()/3))
        self.dropdown = QComboBox(self)
        self.dropdown.addItems(["Food", "Groceries", "shopping", "other"])
        self.amount = QLineEdit()
        int_validator = QIntValidator(0, 999999999)
        self.amount.setValidator(int_validator)
        self.description = QLineEdit(self)

        row2.addWidget(self.dropdown)
        row2.addWidget(self.amount)
        row2.addWidget(self.description)
        row2.addSpacing(int(self.screen_manager.width()/3))

        # third row
        row3 = QHBoxLayout(self)
        row3.addSpacing(int(self.screen_manager.width()/3))

        self.add_button = QPushButton("Add Expense", self)
        self.add_button.clicked.connect(self.add_expense)
        self.delete_button = QPushButton("Delete Expense", self)

        row3.addWidget(self.add_button)
        row3.addWidget(self.delete_button)
        row3.addSpacing(int(self.screen_manager.width()/3))

        # fourth row
        row4 = QHBoxLayout(self)
        row4.addSpacing(int(self.screen_manager.width()/3))

        table_columns = 3
        table_rows = 10
        for i in range(31):
            table = QTableWidget(table_rows, table_columns, self)
            table.setHorizontalHeaderLabels(["Category", "Amount", "Description"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.adjust_table_height(table)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table.verticalHeader().setVisible(False)
            table_style(table)
            if i != datetime.today().day:
                table.hide()
            else:
                table.show()
            self.tables.append(table)
            row4.addWidget(table)

        row4.addSpacing(int(self.screen_manager.width()/3))

        main_layout.addLayout(row1)
        main_layout.addSpacing(50)
        main_layout.addLayout(row2)
        main_layout.addLayout(row3)
        main_layout.addLayout(row4)
        self.setLayout(main_layout)

    def on_frame_click(self, frame, *args):
        for i, box in enumerate(self.calendar_boxes):
            if hasattr(box, 'selected') and box.selected:  # don't affect the day labels (Sun, Mon...)
                box.setStyleSheet("background-color: white;")
                self.tables[i].hide()
                box.selected = False
        frame.selected = True
        frame.setStyleSheet("background-color: gray;")


    def create_calendar(self):
        self.calendar_boxes = []
        for i in range(31):
            frame = ClickableFrame(self)
            frame.setStyleSheet("background-color: white;")
            frame.setMaximumSize(90, 90)
            frame.setFrameShape(QFrame.StyledPanel)
            frame.clicked.connect(lambda qframe=frame: self.on_frame_click(qframe))
            frame.clicked.connect(self.show_day_table)
            frame_layout = QHBoxLayout(frame)
            day_num = QLabel(str(i), frame)
            day_num.setAlignment(Qt.AlignTop)
            frame_layout.addWidget(day_num)
            if i == datetime.today().day:
                frame.click()  # select the frame corresponding to the current daty of the month
            self.calendar_boxes.append(frame)

        self.create_day_labels()

        now = datetime.now()
        current_year = now.year
        current_month = now.month
        days_in_month = calendar.monthrange(current_year, current_month)[1]

        # Get the first day of the month (0 = Monday, 6 = Sunday)
        first_day_of_month = calendar.monthrange(current_year, current_month)[0]
        print(f"this is the first_day_of_month {first_day_of_month}")

        day_counter = 0
        for row in range(1, 7):
            for col in range(7):
                if row == 1 and col < first_day_of_month:
                    continue  # Skip the cells before the first day of the month
                if day_counter <= days_in_month:
                    self.grid.addWidget(self.calendar_boxes[day_counter], row, col)
                    day_counter += 1

    def add_expense(self):
        category = self.dropdown.currentText()
        amount = int(self.amount.text().replace(',', ''))
        description = str(self.description.text())
        inserted_data = [category, amount, description]

        first_key_with_null = None
        # find the first key with a null value
        for key, value in self.data.items():
            if not value:
                first_key_with_null = key
                print(first_key_with_null)
                break
        if first_key_with_null:
            self.data[first_key_with_null] = inserted_data

            for column, item in enumerate(inserted_data):
                table_item = QTableWidgetItem(str(item))
                self.day_table.setItem(first_key_with_null - 1, column, table_item)
            self.db.insert_json_data(self.data, first_key_with_null, self.screen_manager.name)

    # shows the table for the relevant day of the month
    def show_day_table(self):
        for i, frame in enumerate(self.calendar_boxes):
            if frame.selected:
                self.tables[i].show()


    def adjust_table_height(self, table: QTableWidget):
        row_height = 0
        for row in range(table.rowCount()):
            row_height += table.rowHeight(row)

        header_height = table.horizontalHeader().height()
        total_height = row_height + header_height
        table.setFixedHeight(total_height)

    def create_day_labels(self):
        # font for day labels
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sunday']
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