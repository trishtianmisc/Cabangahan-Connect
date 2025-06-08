from PyQt5 import QtCore, QtGui, QtWidgets, uic
from DATABASE.database import Database
from RESIDENTCOMPLAINT.non_resident_oop import ResidentComp
from LIST_OF_NON_CABANGAHAN_COMPLAINTS.non_list import NonListOfComplaints
import os
from datetime import datetime


class NonResidentComplaintsWidget(QtWidgets.QWidget):

    def __init__(self, official_id=None, list_widget=None):
        super().__init__()
        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()
        print("Resident complaints loaded!")

        ui_path = os.path.join(os.path.dirname(__file__), "non_residentcomplaint.ui")
        uic.loadUi(ui_path, self)

        # Connect buttons
        self.submitimg.clicked.connect(self.residentComplaint)
        self.clear.clicked.connect(self.clear_fields)
        self.list_widget = list_widget
        self.official_id = official_id
        self.non_listofcomplaints.clicked.connect(self.show_non_list_complaints)


        if self.list_widget is None:
            self.non_list_of_complaints_widget = NonListOfComplaints()
        else:
            self.non_list_of_complaints_widget = self.list_widget

    def residentComplaint(self):
        try:
            # Get and trim inputs
            complainant = self.complainant.text().strip()
            address = self.address.text().strip()  # this is address field
            place = self.place.text().strip()  # this is place field
            type_of_complainant = self.complainttype.text().strip()  # get this field from UI
            date_input = self.date.date().toString("yyyy-MM-dd")
            details = self.details.text().strip()

            # Check if any field is blank
            if not all([complainant, address, place, type_of_complainant, date_input, details]):
                QtWidgets.QMessageBox.warning(self, "Missing Fields", "Please fill in all the fields.")
                return False

            # Optional: Validate official ID
            if not isinstance(self.official_id, int):
                QtWidgets.QMessageBox.warning(self, "Invalid Official", "Official ID is not set or invalid.")
                return False

            # Create ResidentComp object
            resident_complaint = ResidentComp(
                None,
                complainant,
                address,
                place,
                type_of_complainant,
                date_input,
                details,
                self.official_id
            )

            query = ("""
                INSERT INTO non_cabangahan_complaints
                (NON_COMPLAINANT, NON_ADDRESS, NON_PLACE, NON_TYPE_OF_COMPLAINANT, COMPLAINT_DATE, DETAILS, OFFICIAL_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)
            values = (
                resident_complaint.complainant,
                resident_complaint.address,
                resident_complaint.place,
                resident_complaint.type_of_complainant,
                resident_complaint.date,
                resident_complaint.details,
                resident_complaint.official_id
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            print("DATA INSERTED")

            # Show success and update list
            self.non_list_of_complaints_widget.show_non_list_of_complaints()
            QtWidgets.QMessageBox.information(self, "Success", "Complaint submitted successfully!")

            self.clear_fields()
            return True

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            return False

    def clear_fields(self):
        self.complainant.clear()
        self.address.clear()
        self.complainttype.clear()
        self.date.clear()
        self.details.clear()

    def show_non_list_complaints(self):
        self.non_list_of_complaints_widget.setWindowFlags(QtCore.Qt.Window)
        self.non_list_of_complaints_widget.show()
        self.non_list_of_complaints_widget.raise_()
        self.non_list_of_complaints_widget.activateWindow()




