
import os
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem

from Secretary.DATABASE.database import Database
from Secretary.LIST_OF_COMPLAINTS.view_complaint import ViewComplaints
from Secretary.RESIDENTCOMPLAINT.resident_OOP import ResidentComp

from functools import partial
class ListOfComplaints(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        print("List of complaints loaded!")
        ui_path = os.path.join(os.path.dirname(__file__), "listofcomplaints.ui")
        uic.loadUi(ui_path, self)

        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()

        self.show_list_of_complaints()
        self.deletebutton.clicked.connect(self.delete_complaint)
        self.searchbar.textChanged.connect(self.search_complaint)
        self.searchbar.setPlaceholderText("Search complaints...")
        self.complaints.horizontalHeader().setStretchLastSection(True)
        self.complaints.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.complaints.verticalHeader().setVisible(False)

    def show_list_of_complaints(self):
        try:
            # Fetch all necessary data including complaint_id
            self.cursor.execute("""
                SELECT COMPLAINT_ID, COMPLAINANT, RESIDENT_ID, TYPE_OF_COMPLAINT, DATE, DETAILS, STATUS
                FROM COMPLAINTS
            """)
            data = self.cursor.fetchall()

            # Set number of rows and columns (7 visible + 1 for button)
            self.complaints.setRowCount(len(data))
            self.complaints.setColumnCount(8)

            # Set headers (including Complaint ID and View Action)
            headers = [
                "Complaint ID", "Complainant", "Resident ID", "Type", "Date",
                "Details", "Status", "Action"
            ]
            self.complaints.setHorizontalHeaderLabels(headers)

            for row_idx, row_data in enumerate(data):
                complaint_id, complainant, resident_id, comp_type, date, details, status = row_data

                self.complaints.setItem(row_idx, 0, QTableWidgetItem(str(complaint_id)))
                self.complaints.setItem(row_idx, 1, QTableWidgetItem(str(complainant)))
                self.complaints.setItem(row_idx, 2, QTableWidgetItem(str(resident_id)))
                self.complaints.setItem(row_idx, 3, QTableWidgetItem(str(comp_type)))
                self.complaints.setItem(row_idx, 4, QTableWidgetItem(str(date)))
                self.complaints.setItem(row_idx, 5, QTableWidgetItem(str(details)))

                # Add a status dropdown (ComboBox)
                combo = QtWidgets.QComboBox()
                combo.addItems(["pending", "solved"])
                combo.setCurrentText(status)
                if status == "solved":
                    combo.setDisabled(True)
                combo.currentTextChanged.connect(partial(self.update_status, complaint_id))
                self.complaints.setCellWidget(row_idx, 6, combo)

                # Add a "View Complaint" button
                btn_view = QtWidgets.QPushButton("View Complaint")
                btn_view.clicked.connect(partial(self.view_complaints_details, complaint_id))
                self.complaints.setCellWidget(row_idx, 7, btn_view)

        except Exception as e:
            print("Error loading complaints list:", e)

    def view_complaints_details(self, complaint_id):
        try:
            # Fetch full complaint details from the database
            self.cursor.execute("""
                SELECT COMPLAINT_ID, COMPLAINANT, RESIDENT_ID, TYPE_OF_COMPLAINT, DATE, DETAILS, STATUS
                FROM COMPLAINTS WHERE COMPLAINT_ID = %s
            """, (complaint_id,))
            result = self.cursor.fetchone()

            if result:
                # Create a complaint object or dictionary
                complaint_data = {
                    "complaint_id": result[0],
                    "complainant": result[1],
                    "resident_id": result[2],
                    "type": result[3],
                    "date": result[4],
                    "details": result[5],
                    "status": result[6]
                }

                # Pass the data to the view window
                self.open_window = ViewComplaints(complaint_data)
                self.open_window.show()
            else:
                QtWidgets.QMessageBox.warning(self, "Not Found", "Complaint not found.")

        except Exception as e:
            print(f"Error opening complaint view: {e}")

    def update_status(self, complaint_obj, new_status):
        try:
            complaint_obj.status = new_status
            query = "UPDATE complaints SET status = %s WHERE complainant = %s AND resident_id = %s"
            self.cursor.execute(query, (new_status, complaint_obj.complainant, complaint_obj.residentID))
            self.conn.commit()
            print(f"Status updated for { complaint_obj.complainant} (Resident ID: "
                  f"{complaint_obj.residentID}): {new_status}")
        except Exception as e:
            print(f"Error updating status: {e}")

    def delete_complaint(self):
        selected_row = self.complaints.currentRow()

        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return
        try:
            # Get the complaint_id text from the first column (column 0)
            item = self.complaints.item(selected_row, 0)
            if item is None:
                raise ValueError("Selected row does not contain a complaint ID.")
            complaint_id = item.text()

            confirm = QtWidgets.QMessageBox.question(
                self, "Confirm Delete", f"Delete complaint ID {complaint_id}?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.Yes:
                self.cursor.execute("DELETE FROM COMPLAINTS WHERE COMPLAINT_ID = %s", (complaint_id,))
                self.conn.commit()
                self.complaints.removeRow(selected_row)
                print(f"Complaint {complaint_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting row: {e}")

    def search_complaint(self, text):
        text = text.lower()
        for row in range(self.complaints.rowCount()):
            show_row = False
            for column in range(self.complaints.columnCount()):
                item = self.complaints.item(row, column)
                if item and text in item.text().lower():
                    show_row = True
                    break
                else:
                    widget = self.complaints.cellWidget(row, column)
                    if isinstance(widget, QtWidgets.QComboBox):
                        if text in widget.currentText().lower():
                            show_row = True
                            break
            self.complaints.setRowHidden(row, not show_row)



