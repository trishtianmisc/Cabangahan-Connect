
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
import os

class NonViewComplaints(QtWidgets.QWidget):
    def __init__(self, complaint_data=None):
        super().__init__()
        print("Non resident ViewComplaints window loaded!")
        ui_path = os.path.join(os.path.dirname(__file__), "view_non_residentcomplaint.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("View Complaint")

        if complaint_data:
            self.findChild(QtWidgets.QLabel, "complainant").setText(complaint_data.get("complainant", ""))
            self.findChild(QtWidgets.QLabel, "address").setText(complaint_data.get("address", ""))
            self.findChild(QtWidgets.QLabel, "place").setText(complaint_data.get("place", ""))
            self.findChild(QtWidgets.QLabel, "complainttype").setText(complaint_data.get("complainttype", ""))
            self.findChild(QtWidgets.QLabel, "date").setText(str(complaint_data.get("complaint_date", "")))
            self.findChild(QtWidgets.QLabel, "details").setText(complaint_data.get("details", ""))

