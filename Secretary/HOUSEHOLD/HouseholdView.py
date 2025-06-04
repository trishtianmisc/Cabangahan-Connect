from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QHeaderView
from PyQt5 import QtCore
from Secretary.DATABASE.database import Database
import sys, os
from Secretary.HOUSEHOLD.HouseholdMemberAdding import HouseholdAddingWindow
from Secretary.RESIDENT.ViewProfile import ViewProfileWindow


class HouseholdViewWindow(QtWidgets.QWidget):
    def __init__(self, stacked_widget, house_id):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "HoseuholdViewUI.ui")
        uic.loadUi(ui_path, self)

        

        self.db = Database()
        self.db.set_connection()
        self.cursor = self.db.get_cursor()

        self.stackedWidget = stacked_widget

        self.house_id = house_id

        self.display_household()
        self.tabledesign()
        self.loadtable()

        self.addmember_btn.clicked.connect(self.addmember_popup)

    def loadtable(self):
        try:
            
            query = "SELECT R.RES_ID, R.RES_FIRSTNAME, R.RES_MIDDLENAME, R.RES_LASTNAME, R.RES_DATEOFBIRTH, HM.HMEM_RELATIONSHIP FROM HOUSEHOLD H JOIN HOUSEHOLD_MEMBER HM ON H.HOUSE_ID = HM.HOUSE_ID " \
            "JOIN RESIDENT R ON HM.RES_ID = R.RES_ID WHERE H.HOUSE_ID = %s"
            
            self.cursor.execute(query, (self.house_id,))
            result = self.cursor.fetchall()
                
            num_data_cols = 6
            self.table_members.setRowCount(len(result))
            

            for row_idx, row_data in enumerate(result):
                for col_idx, value in enumerate(row_data):
                    if col_idx == 4:  # Birthdate column
                        age = self.db.calculate_age(value)
                        item = QtWidgets.QTableWidgetItem(str(age))
                    else:
                        item = QtWidgets.QTableWidgetItem(str(value))
                    self.table_members.setItem(row_idx, col_idx, item)

                view_button = QPushButton("View members")
                view_button.clicked.connect(lambda _, r=row_data: self.show_members(r))
                self.table_members.setCellWidget(row_idx, num_data_cols, view_button)


        except Exception as e:
            print("Failed: ", e)

    def show_members(self, res_id):
        
        self.view_profile = ViewProfileWindow(self.stackedWidget, res_id[0])
        self.stackedWidget.addWidget(self.view_profile)
        self.stackedWidget.setCurrentWidget(self.view_profile)


    def addmember_popup(self):
        self.add_window = HouseholdAddingWindow(self.house_id)
        self.add_window.member_added.connect(self.loadtable)  # reconnect data after insert
        self.add_window.show()


    def display_household(self):

        try:

            query = "SELECT RES_FIRSTNAME, RES_LASTNAME, HOUSE_OWNERSHIP, HOUSE_CONTACT, PUROK_NAME FROM HOUSEHOLD H JOIN RESIDENT R ON H.HOUSE_HEAD = R.RES_ID JOIN PUROK P" \
            " ON H.PUROK_ID = P.PUROK_ID WHERE HOUSE_ID = %s"

            self.cursor.execute(query, (self.house_id,))

            result = self.cursor.fetchone()

            if result:
                full_name = f"{result['res_firstname']} {result['res_lastname']}"
                self.line_head.setText(full_name)
                self.line_ownership.setText(result["house_ownership"])
                self.line_contact.setText(result["house_contact"])
                self.line_purok.setText(result["purok_name"])
            else:
                print("No result found.")

        except Exception as e:
            print("Failed: ", e)




    def tabledesign(self):
        self.table_members.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
 
        self.table_members.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        # 2) Tell the header to stretch all sections
        header = self.table_members.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_members.verticalHeader().setVisible(False)