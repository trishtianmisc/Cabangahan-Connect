from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QButtonGroup, QMessageBox
from PyQt5 import QtGui
from PyQt5 import uic  # import the UI class generated from ProfilingUI.ui
from PyQt5.QtGui import QPixmap
from database import Database
import sys, os

class OfficialWindow(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI', 'OfficialUI.ui'))
        uic.loadUi(ui_path, self)

        self.stackedWidget = stacked_widget

        self.db = Database()
        self.db.set_connection()
        self.cursor = self.db.get_cursor()

        self.official_display()

        self.select_captain.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.select_councilor.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.select_treasurer.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.select_secretary.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))


    def official_display(self):
        
        self.label_captain.hide()
        self.label_councilor.hide()
        self.label_treasurer.hide()
        self.label_secretary.hide()

        try:
            query = "SELECT POS_TYPE, RES_FIRSTNAME, RES_MIDDLENAME, RES_LASTNAME, RES_PROFILEPIC FROM POSITIONTYPE P JOIN OFFICIAL O ON P.POS_ID = O.POS_ID JOIN RESIDENT R ON O.RES_ID = R.RES_ID"
            self.cursor.execute(query)

            result = self.cursor.fetchall()

            for row in result:
                pos_type, first, middle, last, file_path = row
                middle = middle or ""  # Avoid None values
                full_name = f"{first} {middle} {last}".strip()

                if pos_type == "Captain":
                    self.select_captain.hide()
                    self.label_captain.show()
                    self.label_captain.setText(full_name)
                    if file_path:
                        pixmap = QPixmap(file_path)
                        self.captain_pic.setPixmap(pixmap)
                        self.captain_pic.setScaledContents(True)

                elif pos_type == "Councilor":
                    self.select_councilor.hide()
                    self.label_councilor.show()
                    self.label_councilor.setText(full_name)
                    if file_path:
                        pixmap = QPixmap(file_path)
                        self.councilor_pic.setPixmap(pixmap)
                        self.councilor_pic.setScaledContents(True)

                elif pos_type == "Treasurer":
                    self.select_treasurer.hide()
                    self.label_treasurer.show()
                    self.label_treasurer.setText(full_name)
                    if file_path:
                        pixmap = QPixmap(file_path)
                        self.treasurer_pic.setPixmap(pixmap)
                        self.treasurer_pic.setScaledContents(True)

                elif pos_type == "Secretary":
                    self.select_secretary.hide()
                    self.label_secretary.show()
                    self.label_secretary.setText(full_name)
                    if file_path:
                        pixmap = QPixmap(file_path)
                        self.secretary_pic.setPixmap(pixmap)
                        self.secretary_pic.setScaledContents(True)

        except Exception as e:

            print(f"No : {e}")

