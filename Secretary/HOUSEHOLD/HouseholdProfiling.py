from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QButtonGroup, QFileDialog, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import uic  # import the UI class generated from ProfilingUI.ui
from Secretary.DATABASE.database import Database
from Secretary.HOUSEHOLD.HouseholdHeadSelector import ResidentSelectorDialog
import sys, os


class HouseholdProfilingWindow(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "HouseholdProfilingUI.ui")
        uic.loadUi(ui_path, self)

        self.db = Database()
        self.db.set_connection()
        self.cursor = self.db.get_cursor()
        
        self.populate_purokbox()

        self.submit_btn.clicked.connect(self.insert_household)
        self.popup_resident.clicked.connect(self.show_popup)


    def insert_household(self):
        
        contact = self.line_contact.text()
        ownership = self.line_ownership.text()
        purok = self.combo_purok.currentData()

        try:
            query = "INSERT INTO HOUSEHOLD (HOUSE_HEAD, HOUSE_CONTACT, HOUSE_OWNERSHIP, PUROK_ID) VALUES(%s, %s, %s, %s)"

            values = (self.selected_head_id, contact, ownership, purok)

            self.cursor.execute(query, values)
           
            self.db.commit()
            QMessageBox.information(self, "Success", "Household Registered!")


            

        except Exception as e:
                QMessageBox.critical(self, "Insert Failed", f"Inserting Household Failed:\n{e}")
                return False

    
    def populate_purokbox(self):

        try:
            
            query = "SELECT PUROK_ID, PUROK_NAME FROM PUROK" 
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            self.combo_purok.addItem("Select", None)   
            for purok_id, purok_name in results:
               
                self.combo_purok.addItem(purok_name, purok_id)

        except Exception as e:
            print("Failed:", e)
        
    def show_popup(self):
        dialog = ResidentSelectorDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            res_id, full_name, user = dialog.get_selection()
            self.line_head.setText(full_name)
            self.selected_head_id = res_id



