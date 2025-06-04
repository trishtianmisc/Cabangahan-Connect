
import os

from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

from Secretary.LIST_OF_REQUESTS.Income import CertificatesIncome
from Secretary.REQUESTDOCUMENTS.RequestOOP import Request
from Secretary.DATABASE.database import Database
from PyQt5 import QtWidgets, uic

class ListRequests(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        print("LIST OF REQUEST LOADED")
        ui_path = os.path.join(os.path.dirname(__file__), "listofrequests.ui")
        uic.loadUi(ui_path, self)



        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()
        self.show_list_of_request()
        self.searchbar.setPlaceholderText("Search complaints...")
        self.searchbar.textChanged.connect(self.search_request)

        self.request.horizontalHeader().setStretchLastSection(True)
        self.request.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.request.verticalHeader().setVisible(False)


        self.purchases.clicked.connect(self.show_purchases)
        self.deletebutton.clicked.connect(self.delete_purchases)

    def show_list_of_request(self):
        try:
            self.cursor.execute("""
                SELECT RD.DOCUMENT_ID,R.RES_ID, R.RES_FIRSTNAME, R.RES_LASTNAME, R.RES_MIDDLENAME, RD.CERTIFICATE_TYPE , RD.PRICE
                FROM RESIDENT AS R 
                INNER JOIN REQUEST_DOCUMENT AS RD ON R.RES_ID = RD.RESIDENT_ID
            """)
            data = self.cursor.fetchall()


            self.request.setRowCount(len(data))
            self.request.setColumnCount(7)
            self.request.setHorizontalHeaderLabels([
               "Document ID", "Resident ID", "First Name", "Last Name", "Middle Name", "Certificate Type" , "Request Fee"
            ])




            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.request.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.request.setColumnHidden(0, True)
        except Exception as e:
            print("Error loading request list:", e)

    def show_purchases(self):
        self.purchase_window = CertificatesIncome()
        self.purchase_window.show()

    def delete_purchases(self):
        selected_row = self.request.currentRow()

        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return

        try:

            document_id_item = self.request.item(selected_row, 0)

            if not document_id_item:
                QtWidgets.QMessageBox.warning(self, "Invalid Selection", "Cannot find Document ID.")
                return

            document_id = document_id_item.text()

            confirm = QtWidgets.QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete this request (Document ID: {document_id})?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if confirm == QtWidgets.QMessageBox.Yes:

                self.cursor.execute("DELETE FROM REQUEST_DOCUMENT WHERE DOCUMENT_ID = %s", (document_id,))
                self.conn.commit()


                self.request.removeRow(selected_row)

                QtWidgets.QMessageBox.information(self, "Deleted", "Request deleted successfully.")

        except Exception as e:
            print("Error deleting request:", e)
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to delete: {e}")

    def search_request(self, text):
        text = text.lower().strip()
        for row in range(self.request.rowCount()):
            show_row = False
            for column in range(self.request.columnCount()):
                item = self.request.item(row, column)
                if item and text in item.text().lower():
                    show_row = True
                    break

                widget = self.request.cellWidget(row, column)
                if isinstance(widget, QtWidgets.QComboBox):
                    if text in widget.currentText().lower():
                        show_row = True
                        break

            self.request.setRowHidden(row, not show_row)
