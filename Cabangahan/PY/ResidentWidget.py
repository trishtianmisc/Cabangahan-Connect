from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore

from database import Database
import sys, os
from ProfilingWidget import ProfilingWindow
from ViewProfile import ViewProfileWindow


class ResidentWindow(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI', 'ResidentUI.ui'))
        uic.loadUi(ui_path, self)


        self.db = Database()
        self.db.set_connection()
        self.cursor = self.db.get_cursor()

        self.stacked_widget = stacked_widget

        self.addbutton.clicked.connect(self.show_add)
        self.line_search.textChanged.connect(self.apply_filters)
        self.combo_age.currentIndexChanged.connect(self.apply_filters)
        self.combo_registered.currentIndexChanged.connect(self.apply_filters)
        self.combo_purok.currentIndexChanged.connect(self.apply_filters)
        

        self.tabledesign()
        self.loadtable()

    def show_add(self):
        
        self.profiling = ProfilingWindow(self)
        self.stacked_widget.insertWidget(2, self.profiling)
        self.stacked_widget.setCurrentIndex(2)

    def show_profile(self, row_data):

        res_id = row_data[0]

        self.viewprofile = ViewProfileWindow(res_id)
        self.stacked_widget.insertWidget(3, self.viewprofile)

        self.stacked_widget.setCurrentIndex(3)

    def apply_filters(self):
        search = self.line_search.text()
        age = self.combo_age.currentText()
        registered = self.combo_registered.currentText()
        purok = self.combo_purok.currentText()

        self.loadtable(search, age, registered, purok)


    def loadtable(self, search="", age=None, registered=None, purok=None):
        query = """
            SELECT RES_ID, RES_FIRSTNAME, RES_LASTNAME, RES_MIDDLENAME, RES_PUROK 
            FROM RESIDENT
            WHERE 1=1
        """
        values = []

        if search:
            query += """ AND (
                RES_FIRSTNAME ILIKE %s OR
                RES_LASTNAME ILIKE %s OR
                RES_MIDDLENAME ILIKE %s
            )"""
            search_term = f"%{search}%"
            values.extend([search_term, search_term, search_term])

        if registered and registered != "All":
            query += " AND RES_REGISTERED = %s"
            values.append(registered)

        if purok and purok != "All":
            query += " AND RES_PUROK = %s"
            values.append(purok)

        if age and age != "All":
            if age == "18 and below":
                query += " AND DATE_PART('year', AGE(RES_DATEOFBIRTH)) <= 18"
            elif age == "19-59":
                query += " AND DATE_PART('year', AGE(RES_DATEOFBIRTH)) BETWEEN 19 AND 59"
            elif age == "60 and above":
                query += " AND DATE_PART('year', AGE(RES_DATEOFBIRTH)) >= 60"

        self.cursor.execute(query, values)
        data = self.cursor.fetchall()

        self.tableresidents.setRowCount(len(data))
        self.tableresidents.setColumnCount(6)

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.tableresidents.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

            view_button = QPushButton("View Profile")
            view_button.clicked.connect(lambda _, r=row_data: self.show_profile(r))
            self.tableresidents.setCellWidget(row_idx, 5, view_button)


    def view_resident(self, row_data):
        res_id = row_data[0]
        print(f"View button clicked for resident ID: {res_id}")
        # You can open a detailed dialog or new window here

    def tabledesign(self):
        self.tableresidents.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.tableresidents.setColumnWidth(0, 80)   # RES_ID
        self.tableresidents.setColumnWidth(1, 300)  # First Name
        self.tableresidents.setColumnWidth(2, 300)  # Last Name
        self.tableresidents.setColumnWidth(3, 300)  # Middle Name
        self.tableresidents.setColumnWidth(4, 220)  # Purok
        self.tableresidents.setColumnWidth(5, 120)  # Button
        self.tableresidents.verticalHeader().setVisible(False)
