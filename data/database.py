import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox


class DatabaseManager:

    def __init__(self):
        self.create_connection()
        self.create_table()
        # self.print_table_schema()
        self.plan_dict = {}
        self.fetch_plan()
        print(self.plan_dict)

    def create_connection(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("C:/Users/sanad/planner/general_info.db")
        if not self.db.open():
            QMessageBox.Critical(None, "Error", "Could not open your db")
            sys.exit(1)
        else:
            print("Database connected successfully.")

    def create_table(self):
        query = QSqlQuery()

        # query.exec_("DROP TABLE IF EXISTS answers")

        query.exec_('''CREATE TABLE IF NOT EXISTS answers
                               (name TEXT NULL PRIMARY KEY, income REAL, rent REAL, utilities REAL,
                                bills REAL, transportation REAL, loans REAL,
                                budget REAL)''')
    '''
    @staticmethod
    def print_table_schema():
        query = QSqlQuery()
        query.exec_("PRAGMA table_info(answers);")
        while query.next():
            column_id = query.value(0)
            column_name = query.value(1)
            column_type = query.value(2)
            is_not_null = query.value(3)
            default_value = query.value(4)
            is_primary_key = query.value(5)
            print(f"Column ID: {column_id}, Name: {column_name}, Type: {column_type}, "
                  f"Not Null: {is_not_null}, Default: {default_value}, Primary Key: {is_primary_key}")
                  '''

    def get_percentages(self, plan_name):
        query = QSqlQuery()
        query.prepare('''SELECT income, rent, utilities, bills, transportation, loans, budget 
                             FROM answers WHERE name = :name ORDER BY rowid DESC''')

        # Bind the parameter value
        query.bindValue(':name', plan_name)

        # Execute the query
        if query.exec_():
            if query.next():
                print("Data retrieved successfully")
                income = query.value(0)

                if income is not None:
                    print(f"this the income: {income}, rent: {query.value(1)}, util: {query.value(2)}"
                          f"bills {query.value(3)}, transportation: {query.value(4)}, loans: {query.value(5)}"
                          f"budget: {query.value(6)}")
                    print(query.value(1))
                    return {
                        "income": income,
                        "rent": round((query.value(1) / income) * 100, 1),
                        "utilities": round((query.value(2) / income) * 100, 1),
                        "bills": round((query.value(3) / income) * 100, 1),
                        "transportation": round((query.value(4) / income) * 100, 1),
                        "loans": round((query.value(5) / income) * 100, 1),
                        "budget": round((query.value(6) / income) * 100, 1)
                    }

                else:
                    print("Income is None or zero, cannot calculate percentages")
            else:
                print("No data found")
        return {}

    def insert_plan_name(self, name):
        query = QSqlQuery()

        query.prepare('''INSERT INTO answers (name)
                                     VALUES (?)''')
        query.addBindValue(name)

        if not query.exec_():
            # Detailed error handling
            error = query.lastError()
            print(f"Error inserting data: {error.text()}")
            print(f"SQL query: {query.executedQuery()}")
        else:
            print("Name inserted successfully.")

    # for loading a plan
    def fetch_plan(self):
        query = QSqlQuery()
        names = []
        if query.exec_("SELECT name, income FROM answers ORDER BY rowid DESC"):
            while query.next():
                name = query.value(0)
                income = query.value(1)
                self.plan_dict[name] = income
                names.append(name)

        else:
            print("failed to fetch name")
            # return a list of plan names and a dict that contains names and income values
        return names, self.plan_dict

   # def load_plan(self, plan_name: dict, key):
