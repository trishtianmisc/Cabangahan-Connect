from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QButtonGroup, QFileDialog, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from Secretary.DATABASE.database import Database
from Secretary.HOUSEHOLD.HouseholdMemberSelector import ResidentSelectorDialog
import sys, os


class HouseholdAddingWindow(QtWidgets.QWidget):

    member_added = pyqtSignal()

    def __init__(self, house_id):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "HouseholdMemberAddingUI.ui")
        uic.loadUi(ui_path, self)

        self.db = Database()
        self.db.set_connection()
        self.cursor = self.db.get_cursor()

        self.house_id = house_id

        self.member_btn.clicked.connect(self.show_popup)
        self.confirm_btn.clicked.connect(self.insert_member)

    
    def insert_member(self):
        relationship = self.line_relationship.text()

        try:
            query = "INSERT INTO HOUSEHOLD_MEMBER(HMEM_RELATIONSHIP, HOUSE_ID, RES_ID) VALUES (%s, %s, %s)"
            
            values = (relationship, self.house_id, self.selected_member_id)

            self.cursor.execute(query, values)

            self.db.commit()
            QMessageBox.information(self, "Success", "Household Member Registered!")
            self.member_added.emit()  # signal emitted!
            self.close()


            

        except Exception as e:
                QMessageBox.critical(self, "Insert Failed", f"Inserting Household Member Failed:\n{e}")
                return False
        

    
    def show_popup(self):
        dialog = ResidentSelectorDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            res_id, full_name, user = dialog.get_selection()
            self.line_member.setText(full_name)
            self.selected_member_id = res_id
            

