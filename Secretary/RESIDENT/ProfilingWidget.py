from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QButtonGroup, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import uic  # import the UI class generated from ProfilingUI.ui
from Secretary.DATABASE.database import Database
import sys, os


class ProfilingWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "ProfilingUI.ui")
        uic.loadUi(ui_path, self)


        self.button_group = QButtonGroup()
        self.gender_group = QButtonGroup()
        
        self.db = Database()    

        self.db.set_connection()
        self.cursor = self.db.get_cursor()

        self.groupbutton()

        self.submitbutton.clicked.connect(self.getdata)

        self.pic_button.clicked.connect(self.attach_file)


    
    def attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.pic_label.setPixmap(pixmap)
            self.pic_label.setScaledContents(True)   
    
    def getdata(self):

        image_path = getattr(self, 'image_path', None)
        firstname = self.line_firstname.text()
        lastname = self.line_lastname.text()
        middlename = self.line_middlename.text()
        dob = self.date_dob.date().toString("yyyy-MM-dd")
        pob = self.line_pob.text()
        nationality = self.line_nationality.text()
        religion = self.line_religion.text()
        purok = self.combo_purok.currentText()
        
        
        gender = self.gender_group.checkedButton().text()

        pwd = "Yes" if self.check_pwd.isChecked() else "No"
        registered = "Yes" if self.check_registered.isChecked() else "No"

        bloodtype = self.combo_bloodtype.currentText()
        height = self.line_height.text()
        weight = self.line_weight.text()
        civilstatus = self.button_group.checkedButton().text()
        

        query = """
            INSERT INTO RESIDENT (
            RES_FIRSTNAME, RES_LASTNAME, RES_MIDDLENAME, RES_DATEOFBIRTH, RES_PLACEOFBIRTH, RES_NATIONALITY,
            RES_RELIGION, RES_PUROK, RES_GENDER, RES_PWD, RES_REGISTERED, RES_BLOODTYPE,
            RES_HEIGHT, RES_WEIGHT, RES_CIVILSTATUS, RES_PROFILEPIC
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (
                firstname, lastname, middlename, dob, pob, nationality,
                religion, purok, gender, pwd, registered, bloodtype,
                height, weight, civilstatus, image_path
            )
        try:

            self.cursor.execute(query, values)
            # ✅ Broadcast update

          
            self.db.commit()

            
            

        except Exception as e:
          print(f"Inserting Resident Failed {e}")
          return False



    def groupbutton(self):
        
        self.button_group.addButton(self.radioButton_3)
        self.button_group.addButton(self.radioButton_4)
        self.button_group.addButton(self.radioButton_5)
        self.button_group.addButton(self.radioButton_6)
        self.button_group.addButton(self.radioButton_7)
        self.button_group.addButton(self.radioButton_8)

        
        self.gender_group.addButton(self.radioButton)
        self.gender_group.addButton(self.radioButton_2)


