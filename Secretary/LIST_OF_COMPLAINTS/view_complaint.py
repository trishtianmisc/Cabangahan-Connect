
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
import os

class ViewComplaints(QtWidgets.QWidget):

    def __init__(self, complaint_data=None):
        super().__init__()

        print("ViewComplaints window loaded!")
        ui_path = os.path.join(os.path.dirname(__file__), "view complaint.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("View Complaint")

        if complaint_data:
            self.findChild(QtWidgets.QLabel, "complainant").setText(complaint_data.get("complainant", ""))
            self.findChild(QtWidgets.QLabel, "residenid").setText(str(complaint_data.get("resident_id", "")))
            self.findChild(QtWidgets.QLabel, "typeofcomplaint").setText(complaint_data.get("type", ""))
            self.findChild(QtWidgets.QLabel, "date").setText(str(complaint_data.get("date", "")))
            self.findChild(QtWidgets.QLabel, "details").setText(complaint_data.get("details", ""))
