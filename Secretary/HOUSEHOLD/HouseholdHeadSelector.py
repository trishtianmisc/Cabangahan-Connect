from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QHeaderView
import os
from Secretary.DATABASE.database import Database

class ResidentSelectorDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "HouseholdMemberSelectorUI.ui")
        uic.loadUi(ui_path, self)

        self.current_page = 0
        self.page_size = 10
        self.selected_id = None
        self.selected_name = None
        
        self.table_members.verticalHeader().setVisible(False)
        self.table_members.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.search_bar.textChanged.connect(self.load_data)
        self.table_members.cellDoubleClicked.connect(self.select_resident)

        self.load_data()

    def load_data(self):
        self.table_members.setRowCount(0)
        self.db = Database()
        self.db.set_connection()
        cursor = self.db.get_cursor()

        term = self.search_bar.text().strip()
        like_term = f"%{term}%"

        query = """
        SELECT r.RES_ID, r.RES_FIRSTNAME, r.RES_MIDDLENAME, r.RES_LASTNAME
        FROM RESIDENT r
        LEFT JOIN household_member hm ON r.RES_ID = hm.RES_ID
        LEFT JOIN household h on r.RES_ID = h.HOUSE_HEAD
        WHERE (r.RES_FIRSTNAME ILIKE %s
            OR r.RES_MIDDLENAME ILIKE %s
            OR r.RES_LASTNAME ILIKE %s)
            AND hm.RES_ID IS NULL
            and h.HOUSE_HEAD IS NULL
        ORDER BY r.RES_LASTNAME, r.RES_FIRSTNAME
    """
        cursor.execute(query, (like_term, like_term, like_term))
        rows = cursor.fetchall()

        for row_idx, row in enumerate(rows):
            self.table_members.insertRow(row_idx)
            for col_idx, value in enumerate(row):
                self.table_members.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def select_resident(self, row, column):
        self.selected_id = int(self.table_members.item(row, 0).text())
        first = self.table_members.item(row, 1).text()
        middle = self.table_members.item(row, 2).text()
        last = self.table_members.item(row, 3).text()
        self.selected_name = f"{first} {last}"
        self.user = f"{first}{self.selected_id}"
        self.accept()

    def get_selection(self):
        return self.selected_id, self.selected_name, self.user
