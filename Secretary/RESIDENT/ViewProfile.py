from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QButtonGroup, QMessageBox
from PyQt5.QtWidgets import QButtonGroup, QFileDialog
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
from PyQt5 import uic  # import the UI class generated from ProfilingUI.ui
from Secretary.DATABASE.database import Database
import sys, os

class ViewProfileWindow(QtWidgets.QWidget):
    def __init__(self, stackedWidget, RES_ID):

        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "ViewProfileUI.ui")
        uic.loadUi(ui_path, self)

        self.db = Database

        self.db.set_connection

        self.cursor = self.db.get_cursor

        self.stackedWidget = stackedWidget

        self.RES_ID = RES_ID
        self.firstname = ""
        self.pic_button.clicked.connect(self.attach_file)
        self.label_resid.setText(str(RES_ID))
        self.pic_button.hide()
        self.update_button.hide()
        self.cancel_button.hide()

        self.db = Database()
        self.db.set_connection()    
        self.cursor = self.db.get_cursor()

        self.populatedata()
        self.householdview_btn.hide()
        self.checkhousehold()
        
        self.householdview_btn.clicked.connect(self.viewhousehold)
        self.householdassign_btn.clicked.connect(self.assignhousehold)
        
        self.edit_button.clicked.connect(self.updateprofile)
        self.cancel_button.clicked.connect(self.cancelupdateprofile)
        self.update_button.clicked.connect(self.updatetodatabase)

    def checkhousehold(self):

        try:
            query = "SELECT HOUSE_ID FROM HOUSEHOLD WHERE HOUSE_HEAD = %s " \
            "UNION " \
            "SELECT HOUSE_ID FROM HOUSEHOLD_MEMBER WHERE RES_ID = %s"

            self.cursor.execute(query, (self.RES_ID, self.RES_ID))

            result = self.cursor.fetchone()
            if result:
                
                self.house_id = result["house_id"]
                self.householdview_btn.show()
                self.householdassign_btn.hide()
                self.householdview_btn.setText(str(self.house_id))
            



        except Exception as e:
          print(f"No information: {e}")
          return False
        
    def viewhousehold(self):

        from HouseholdView import HouseholdViewWindow
        self.view_household = HouseholdViewWindow(self.stackedWidget, self.house_id)
        self.stackedWidget.addWidget(self.view_household)
        self.stackedWidget.setCurrentWidget(self.view_household)

    def assignhousehold(self):

        from Household import HouseholdWindow
        self.assign_household = HouseholdWindow(self.stackedWidget)
        self.stackedWidget.addWidget(self.assign_household)
        self.stackedWidget.setCurrentWidget(self.assign_household)

    def populatedata(self):

        
        try:
            query = "SELECT * FROM RESIDENT WHERE RES_ID = %s"
            self.cursor.execute(query, (self.RES_ID, ))
            result = self.cursor.fetchone()

            if result:
                
                self.line_firstname.setText(str(result["res_firstname"]))
                self.line_middlename.setText(str(result["res_middlename"]))
                self.line_lastname.setText(str(result["res_lastname"]))

                dob = result["res_dateofbirth"]
                self.date_dob.setDate(QDate(dob.year, dob.month, dob.day))
                self.line_pob.setText(str(result["res_placeofbirth"]))
                self.line_nationality.setText(str(result["res_nationality"]))
                self.line_religion.setText(str(result["res_religion"]))
                self.line_bloodtype.setText(str(result["res_bloodtype"]))
                self.line_registered.setText(str(result["res_registered"]))
                self.line_purok.setText(str(result["res_purok"]))
                self.line_height.setText(str(result["res_height"]))
                self.line_weight.setText(str(result["res_weight"]))
                self.line_civilstatus.setText(str(result["res_civilstatus"]))
                self.line_gender.setText(str(result["res_gender"]))
                self.line_pwd.setText(str(result["res_pwd"]))

                self.file_path = str(result["res_profilepic"])

                if self.file_path:
                    pixmap = QPixmap(self.file_path)
                    self.pic_label.setPixmap(pixmap)
                    self.pic_label.setScaledContents(True)  
                


                

        except Exception as e:
          print(f"No information: {e}")
          return False
        

    def attach_file(self):
            self.pic_change, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*)")
            if self.pic_change:
                
                pixmap = QPixmap(self.pic_change)
                self.pic_label.setPixmap(pixmap)
                self.pic_label.setScaledContents(True)  
                self.pic_label.show()
                self.pic_button.hide()

                
    def updateprofile(self):
        self.update_button.show()
        self.cancel_button.show()
        self.edit_button.hide()

        self.line_firstname.setEnabled(True)
        self.line_middlename.setEnabled(True)
        self.line_lastname.setEnabled(True)
        
        self.date_dob.setEnabled(True)
        self.line_pob.setEnabled(True)
        self.line_nationality.setEnabled(True)
        self.line_religion.setEnabled(True)
        self.line_bloodtype.setEnabled(True)
        self.line_registered.setEnabled(True)
        self.line_purok.setEnabled(True)
        self.line_height.setEnabled(True)
        self.line_weight.setEnabled(True)
        self.line_civilstatus.setEnabled(True)
        self.line_gender.setEnabled(True)
        self.line_pwd.setEnabled(True)
        self.pic_button.show()
        self.pic_label.hide()

    def cancelupdateprofile(self):

        reply = QMessageBox.question(
        self,
        "Cancel Update",
        "Are you sure you want to cancel editing the profile?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
      )

        if reply == QMessageBox.Yes:
            self.update_button.hide()
            self.cancel_button.hide()
            self.edit_button.show()
            self.line_firstname.setEnabled(False)
            self.line_middlename.setEnabled(False)
            self.line_lastname.setEnabled(False)

            self.date_dob.setEnabled(False)
            self.line_pob.setEnabled(False)
            self.line_nationality.setEnabled(False)
            self.line_religion.setEnabled(False)
            self.line_bloodtype.setEnabled(False)
            self.line_registered.setEnabled(False)
            self.line_purok.setEnabled(False)
            self.line_height.setEnabled(False)
            self.line_weight.setEnabled(False)
            self.line_civilstatus.setEnabled(False)
            self.line_gender.setEnabled(False)
            self.line_pwd.setEnabled(False)
            self.pic_button.hide()
            self.pic_label.show()

    def updatetodatabase(self):

        firstname = self.line_firstname.text()
        lastname = self.line_lastname.text()
        middlename = self.line_middlename.text()
        dob = self.date_dob.date().toString("yyyy-MM-dd")
        pob = self.line_pob.text()
        nationality = self.line_nationality.text()
        religion = self.line_religion.text()
        purok = self.line_purok.text()

        gender = self.line_gender.text()
        civilstatus = self.line_civilstatus.text()
        pwd = "Yes" if self.line_pwd == "Yes" else "No"
        registered = "Yes" if self.line_registered == "Yes" else "No"

        bloodtype = self.line_bloodtype.text()
        height = self.line_height.text()
        weight = self.line_weight.text()
        

        query = """
                UPDATE RESIDENT SET
                    RES_FIRSTNAME = %s,
                    RES_LASTNAME = %s,
                    RES_MIDDLENAME = %s,
                    RES_DATEOFBIRTH = %s,
                    RES_PLACEOFBIRTH = %s,
                    RES_NATIONALITY = %s,
                    RES_RELIGION = %s,
                    RES_PUROK = %s,
                    RES_GENDER = %s,
                    RES_PWD = %s,
                    RES_REGISTERED = %s,
                    RES_BLOODTYPE = %s,
                    RES_HEIGHT = %s,
                    RES_WEIGHT = %s,
                    RES_CIVILSTATUS = %s,
                    RES_PROFILEPIC = %s
                WHERE RES_ID = %s
            """

        values = (
                firstname, lastname, middlename, dob, pob, nationality,
                religion, purok, gender, pwd, registered, bloodtype,
                height, weight, civilstatus, self.pic_change, self.RES_ID
            )
        try:

            self.cursor.execute(query, values)

            # ✅ Broadcast update
            self.cursor.execute("NOTIFY resident_update, 'updated';")

            self.db.commit()
            QMessageBox.information(self, "Success", "Resident data has been saved successfully!")


            

        except Exception as e:
                QMessageBox.critical(self, "Insert Failed", f"Inserting Resident Failed:\n{e}")
                return False