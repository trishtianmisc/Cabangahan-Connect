from PyQt5 import QtCore, QtGui
from Secretary.DATABASE.database import Database
from Secretary.RESIDENTCOMPLAINT.resident_OOP import ResidentComp
import os
from PyQt5 import QtWidgets, uic
from Secretary.LIST_OF_COMPLAINTS.lists import ListOfComplaints



class ResidentComplaintsWidget(QtWidgets.QWidget):

    def __init__(self, official_id=None, list_widget=None):
        super().__init__()
        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()
        print("Resident complaints loaded!")

        ui_path = os.path.join(os.path.dirname(__file__), "residentcomplaint.ui")
        uic.loadUi(ui_path, self)

        # Connect buttons
        self.submitimg.clicked.connect(self.residentComplaint)
        self.clear.clicked.connect(self.clear_fields)
        self.list_widget = list_widget
        self.official_id = official_id
        self.listofcomplaints.clicked.connect(self.show_list_complaints)

        self.residentid.textChanged.connect(self.populate_complainant_name)
        if self.list_widget is None:
            self.list_of_complaints_widget = ListOfComplaints()
        else:
            self.list_of_complaints_widget = self.list_widget


    def residentComplaint(self):
        try:
            # Get and trim inputs
            complainant = self.complainant.text().strip()
            residentid_text = self.residentid.text().strip()
            complainttype = self.complainttype.text().strip()
            date_input = self.date.date().toString("yyyy-MM-dd")

            details = self.details.text().strip()

            # Check if any field is blank
            if not all([complainant, residentid_text, complainttype, date_input, details]):
                QtWidgets.QMessageBox.warning(self, "Missing Fields", "Please fill in all the fields.")
                return False

            # Validate resident ID is numeric
            try:
                residentid = int(residentid_text)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Invalid ID", "Resident ID must be a number.")
                return False

           #IF NI EXISTS ANG RESIDENT
            self.cursor.execute("SELECT res_registered_voter FROM RESIDENT WHERE res_id = %s", (residentid,))
            resident_exists = self.cursor.fetchone()
            if not resident_exists:
                QtWidgets.QMessageBox.warning(self, "Invalid ID", "This resident does not exist.")
                return False


            residentcomplaint = ResidentComp(
                None,
                complainant,
                residentid_text,
                complainttype,
                date_input,
                details,
                self.official_id
            )

            # Insert into DB
            query = ("INSERT INTO COMPLAINTS (COMPLAINANT, RESIDENT_ID, TYPE_OF_COMPLAINT, DATE, DETAILS, OFFICIAL_ID) "
                     "VALUES (%s, %s, %s, %s, %s, %s)")
            values = (
                residentcomplaint.complainant,
                residentcomplaint.residentID,
                residentcomplaint.typeOfComplaint,
                residentcomplaint.date,
                residentcomplaint.details,
                self.official_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()
            print("DATA INSERTED")

            # Show success and update list
            self.list_of_complaints_widget.show_list_of_complaints()
            QtWidgets.QMessageBox.information(self, "Success", "Complaint submitted successfully!")

            self.clear_fields()
            return True

        except Exception as e:
            print(f"INSERT check failed: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to submit complaint: {str(e)}")
            return False

    def clear_fields(self):
        self.complainant.clear()
        self.residentid.clear()
        self.complainttype.clear()
        self.date.clear()
        self.details.clear()

    def show_list_complaints(self):
        self.list_of_complaints_widget.setWindowFlags(QtCore.Qt.Window)
        self.list_of_complaints_widget.show()
        self.list_of_complaints_widget.raise_()
        self.list_of_complaints_widget.activateWindow()

    def populate_complainant_name(self):
        residentid_text = self.residentid.text().strip()

        if residentid_text.isdigit():
            residentid = int(residentid_text)
            try:
                self.cursor.execute("""
                       SELECT res_firstname, res_middlename, res_lastname
                       FROM RESIDENT
                       WHERE res_id = %s
                   """, (residentid,))
                result = self.cursor.fetchone()
                if result:
                    firstname, middlename, lastname = result
                    full_name = f"{firstname} {middlename} {lastname}"
                    self.complainant.setText(full_name)
                else:
                    self.complainant.clear()  # Clear if no matching resident
            except Exception as e:
                print(f"Error fetching resident name: {e}")
                self.complainant.clear()
        else:
            self.complainant.clear()  # Clear if input is not a valid number


