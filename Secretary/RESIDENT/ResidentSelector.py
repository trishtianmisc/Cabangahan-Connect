from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QHeaderView
import sqlite3

from Secretary.DATABASE.database import Database

class ResidentSelectorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Head of Household")
        self.resize(800, 700)

        self.current_page = 0
        self.page_size = 10
        self.selected_id   = None
        self.selected_name = None

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "First Name", "Middle Name", "Last nName"])
        self.table.verticalHeader().setVisible(False)

        
        self.table.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search by name…")
        self.layout.addWidget(self.search_bar)
        self.search_bar.textChanged.connect(self.load_data)

        self.layout.addWidget(self.table)

        self.table.cellDoubleClicked.connect(self.select_resident)

        
        

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        self.db = Database()
        self.db.set_connection()
        cursor = self.db.get_cursor()

        # Get the search term, wrap in % for partial matches
        term = self.search_bar.text().strip()
        like_term = f"%{term}%"

        # Query only rows where either first, middle, or last name matches
        query = """
            SELECT RES_ID, RES_FIRSTNAME, RES_MIDDLENAME, RES_LASTNAME
            FROM RESIDENT
            WHERE RES_FIRSTNAME ILIKE %s
                OR RES_MIDDLENAME ILIKE %s
                OR RES_LASTNAME ILIKE %s
            ORDER BY RES_LASTNAME, RES_FIRSTNAME
        """
        cursor.execute(query, (like_term, like_term, like_term))
        rows = cursor.fetchall()

        for row_idx, row in enumerate(rows):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx,
                    QtWidgets.QTableWidgetItem(str(value)))
        

    def select_resident(self, row, column):
        # grab ID from column 0
        self.selected_id = int(self.table.item(row, 0).text())

        # grab first & last names (or however you want to format it)
        resid = self.table.item(row, 0).text()
        first = self.table.item(row, 1).text()
        middle = self.table.item(row, 2).text()
        last  = self.table.item(row, 3).text()
        self.selected_name = f"{first} {last}"
        self.user = f"{first}{resid}"

        self.accept()  # close dialog with Accepted

    def get_selection(self):
        """Return a tuple of (resident_id, full_name)."""
        return self.selected_id, self.selected_name, self.user

    def next_page(self):
        self.current_page += 1
        self.load_data()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_data()
