
import os
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem

from DATABASE.database import Database
from LIST_OF_NON_CABANGAHAN_COMPLAINTS.non_view_complaint import NonViewComplaints

from functools import partial
class NonListOfComplaints(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        print("List of NON-CABANGAHAN complaints loaded!")
        ui_path = os.path.join(os.path.dirname(__file__), "non_listofcomplaints.ui")
        uic.loadUi(ui_path, self)

        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()

        self.show_non_list_of_complaints()
        self.deletebutton.clicked.connect(self.delete_complaint)
        self.searchbar.textChanged.connect(self.search_complaint)
        self.searchbar.setPlaceholderText("Search complaints...")
        self.complaints.horizontalHeader().setStretchLastSection(True)
        self.complaints.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.complaints.verticalHeader().setVisible(False)

    def show_non_list_of_complaints(self):
        try:
            self.cursor.execute("""
                SELECT  non_cabangahan_comp_id, NON_COMPLAINANT, NON_ADDRESS, NON_PLACE, NON_TYPE_OF_COMPLAINANT,
                       COMPLAINT_DATE, DETAILS, STATUS
                FROM NON_CABANGAHAN_COMPLAINTS
            """)
            data = self.cursor.fetchall()

            self.complaints.setRowCount(len(data))
            self.complaints.setColumnCount(9)
            headers = [
                "Complaint ID", "Complainant", "Address", "Place", "Type",
                "Date", "Details", "Status / Action"
            ]
            self.complaints.setHorizontalHeaderLabels(headers)

            for row_idx, row_data in enumerate(data):
                (complaint_id, complainant, address, place, comp_type,
                 date, details, status) = row_data

                self.complaints.setItem(row_idx, 0, QTableWidgetItem(str(complaint_id)))
                self.complaints.setItem(row_idx, 1, QTableWidgetItem(str(complainant)))
                self.complaints.setItem(row_idx, 2, QTableWidgetItem(str(address)))
                self.complaints.setItem(row_idx, 3, QTableWidgetItem(str(place)))
                self.complaints.setItem(row_idx, 4, QTableWidgetItem(str(comp_type)))
                self.complaints.setItem(row_idx, 5, QTableWidgetItem(str(date)))
                self.complaints.setItem(row_idx, 6, QTableWidgetItem(str(details)))

                combo = QtWidgets.QComboBox()
                combo.addItems(["pending", "solved"])
                combo.setCurrentText(status)
                if status == "solved":
                    combo.setDisabled(True)
                combo.currentTextChanged.connect(partial(self.update_status, complaint_id))
                self.complaints.setCellWidget(row_idx, 7, combo)

                # Add a "View Complaint" button
                btn_view = QtWidgets.QPushButton("View Complaint")
                btn_view.clicked.connect(partial(self.view_complaints_details, complaint_id))
                self.complaints.setCellWidget(row_idx, 8, btn_view)

        except Exception as e:
            print("Error loading complaints list:", e)

    def update_status(self, complaint_id, new_status):
        try:
            query = "UPDATE NON_CABANGAHAN_COMPLAINTS SET STATUS = %s WHERE NON_COMPLAINT_ID = %s"
            self.cursor.execute(query, (new_status, complaint_id))
            self.conn.commit()
            print(f"Status updated for complaint {complaint_id}: {new_status}")
        except Exception as e:
            print(f"Error updating status: {e}")

    def delete_complaint(self):
        selected_row = self.complaints.currentRow()

        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return
        try:
            item = self.complaints.item(selected_row, 0)
            if item is None:
                raise ValueError("Selected row does not contain a complaint ID.")
            complaint_id = item.text()

            confirm = QtWidgets.QMessageBox.question(
                self, "Confirm Delete", f"Delete complaint ID {complaint_id}?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.Yes:
                self.cursor.execute("DELETE FROM NON_CABANGAHAN_COMPLAINTS WHERE NON_COMPLAINT_ID = %s", (complaint_id,))
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

    def view_complaints_details(self, complaint_id):
        try:
            # Fetch full complaint details from the NON_CABANGAHAN_COMPLAINTS table
            self.cursor.execute("""
                SELECT non_cabangahan_comp_id, NON_COMPLAINANT, NON_ADDRESS, NON_PLACE, NON_TYPE_OF_COMPLAINANT, 
                       COMPLAINT_DATE, DETAILS, STATUS
                FROM NON_CABANGAHAN_COMPLAINTS WHERE NON_CABANGAHAN_COMP_ID = %s
            """, (complaint_id,))
            result = self.cursor.fetchone()

            if result:
                complaint_data = {
                    "non_cabangahan_comp_id":result[0],
                    "complainant": result[1],
                    "address": result[2],
                    "place": result[3],
                    "complainttype": result[4],
                    "complaint_date": result[5],
                    "details": result[6],
                    "status":result[7]

                }

                self.open_window = NonViewComplaints(complaint_data)
                self.open_window.show()
            else:
                QtWidgets.QMessageBox.warning(self, "Not Found", "Complaint not found.")
        except Exception as e:
            print(f"Error opening complaint view: {e}")
