from PyQt5 import QtWidgets, uic
from Secretary.DATABASE.database import Database
import os
class CertificatesIncome(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        print("LIST OF REQUEST LOADED")
        ui_path = os.path.join(os.path.dirname(__file__), "income.ui")
        uic.loadUi(ui_path, self)

        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()

        self.Display_per_total_certificate()
        self.Total_purchases()
    def Display_per_total_certificate(self):

        try:
            self.cursor.execute("SELECT CERTIFICATE_TYPE, SUM(PRICE) FROM REQUEST_DOCUMENT GROUP BY CERTIFICATE_TYPE")
            data = self.cursor.fetchall()

            for certificate_type, total in data:
                if certificate_type == "Barangay Clearance":
                    self.clearance.setText(f"₱{total:.2f}")
                elif  certificate_type == "Punong Barangay":
                    self.punong.setText(f"₱{total:.2f}")
                elif certificate_type == "Business Permit":
                    self.permit.setText(f"₱{total:.2f}")


        except Exception as e:

            print(f"insert kay ni failed: {e}")
            QtWidgets.QMessageBox.critical(self, "ERROR", f"Something went wrong:\n{str(e)}")
            return False

    def Total_purchases(self):
        try:
            self.cursor.execute("SELECT SUM(PRICE) FROM REQUEST_DOCUMENT")
            data = self.cursor.fetchone()

            if data[0] is not None:
                total = data[0]
            else:
                total = 0

            self.total.setText(f"₱{total:.2f}")



        except Exception as e:

            print(f"insert kay ni failed: {e}")
            QtWidgets.QMessageBox.critical(self, "ERROR", f"Something went wrong:\n{str(e)}")
            return False






