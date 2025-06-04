from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QHeaderView
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5 import uic  # import the UI class generated from ProfilingUI.ui
from Secretary.DATABASE.database import Database
from Secretary.HOUSEHOLD.HouseholdProfiling import HouseholdProfilingWindow
from Secretary.HOUSEHOLD.HouseholdView import HouseholdViewWindow
from Secretary.HOUSEHOLD.HouseholdListener import DBListener
import sys, os


class HouseholdWindow(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "HouseholdUI.ui")
        uic.loadUi(ui_path, self)

        self.listener = DBListener()
        self.listener.notify_signal.connect(self.loadtable)
        self.listener.start()

        self.db = Database()
        self.db.set_connection()
        self.cursor = self.db.get_cursor()

        self.stackedWidget = stacked_widget

        self.household_btn.clicked.connect(self.showprofiling)

        self.tabledesign()
        self.loadtable()


    def showprofiling(self):
        self.household = HouseholdProfilingWindow(self.stackedWidget)

        self.stackedWidget.insertWidget(5, self.household)
        self.stackedWidget.setCurrentIndex(5)

    def loadtable(self):
        
        try:
            
            query = "SELECT H.HOUSE_ID, R.RES_FIRSTNAME || ' ' || R.RES_MIDDLENAME || ' ' || R.RES_LASTNAME AS head_name, H.HOUSE_CONTACT, H.HOUSE_OWNERSHIP, P.PUROK_NAME FROM HOUSEHOLD H " \
            "JOIN RESIDENT R ON H.HOUSE_HEAD = R.RES_ID JOIN PUROK P ON H.PUROK_ID = P.PUROK_ID"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
                
            num_data_cols = 5
            self.table_household.setRowCount(len(result))
            self.table_household.setColumnCount(num_data_cols + 1)

            for row_idx, row_data in enumerate(result):
                for col_idx, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.table_household.setItem(row_idx, col_idx, item)

                view_button = QPushButton("View Household")
                view_button.clicked.connect(lambda _, r=row_data: self.show_household(r))
                self.table_household.setCellWidget(row_idx, num_data_cols, view_button)


        except Exception as e:
            print("Failed: ", e)

    def tabledesign(self):
        self.table_household.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
 
        self.table_household.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        # 2) Tell the header to stretch all sections
        header = self.table_household.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_household.verticalHeader().setVisible(False)

    def show_household(self, data):
        household_id = data[0]

        self.viewhousehold = HouseholdViewWindow(self.stackedWidget, household_id)

        self.stackedWidget.addWidget(self.viewhousehold)
        self.stackedWidget.setCurrentWidget(self.viewhousehold)




