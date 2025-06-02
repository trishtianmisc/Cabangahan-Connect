

from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui

import re
import os

from CERTIFICATES.BarangayClearance import BarangayClearance

from CERTIFICATES.PunongBarangay import PunongBarangay
from CERTIFICATES.BarangayPermitReal import BusinessPermitFinal
from DATABASE.database import Database
from REQUESTDOCUMENTS.RequestOOP import Request
from LIST_OF_REQUESTS.ListOfRequests import ListRequests





class RequestDocumentsWidget(QtWidgets.QWidget):

    def __init__(self, official_id=None):
        super().__init__()
        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()
        self.official_id = official_id


        print("RequestDocumentsWindow loaded!")
        ui_path = os.path.join(os.path.dirname(__file__), "RequestDocument.ui")
        uic.loadUi(ui_path, self)

        self.eligible.hide()
        self.submit.clicked.connect(self.requestDocs)
        self.exportpdf.clicked.connect(self.export_cert_to_pdf)
        #PARAS STACK WIDGET POP UP
        self.barangayClearance = BarangayClearance()
        self.PunongBarangay =PunongBarangay()
        self.BusinessPermit = BusinessPermitFinal()
        self.certificates = {
            "Barangay Clearance":self.barangayClearance,
            "Punong Barangay":self.PunongBarangay,
            "Business Permit":self.BusinessPermit,

        }
        for widget in self.certificates.values():
            self.certificatestackedWidget.addWidget(widget)


        self.typeOfCertificate.currentIndexChanged.connect(self.switch_certificate_form)


        self.load_certificate_types()

        self.listofrequests.clicked.connect(self.show_list_requests)
        self.list_of_request_document_widget = ListRequests()

    def export_cert_to_pdf(self):
        selected_type = self.typeOfCertificate.currentText()
        if selected_type == "Barangay Clearance":
           self.barangayClearance.export_to_pdf()
        elif selected_type == "Punong Barangay":
            self.PunongBarangay.export_to_pdf_certificate()
        elif selected_type == "Business Permit":
            self.BusinessPermit.export_to_pdf_certificate_business()


    def load_certificate_types(self):

        try:
            self.cursor.execute("SELECT certificate_type FROM barangay_certificates")
            types = self.cursor.fetchall()

            self.typeOfCertificate.clear()
            for cert_type in types:
                self.typeOfCertificate.addItem(cert_type[0])
        except Exception as e:
            print(f"Error fetching certificate types: {e}")

    def requestDocs(self):
        try:
            if self.residentid.text().strip() == "":
                QtWidgets.QMessageBox.warning(self, "BLANK", "ENTER RESIDENT ID")
                return

            residentid = int(self.residentid.text())  # can raise ValueError

            self.cursor.execute("SELECT res_registered_voter FROM RESIDENT WHERE res_id = %s", (residentid,))
            resident_exists = self.cursor.fetchone()

            if not resident_exists:
                QtWidgets.QMessageBox.warning(self, "INVALID ID", "THIS RESIDENT DOES NOT EXIST")
                return

            registered_voter = resident_exists[0]
            print(f'Registered voter {registered_voter}')
            if registered_voter.strip().lower() != 'yes':
                self.eligible.show()
                return
            else:
                self.eligible.hide()

            raw_price = self.price.text().strip()
                # Remove currency symbol, commas, and trailing period
            clean_price = re.sub(r'[^\d.]', '', raw_price).rstrip('.')  # Result: '120.00'

            # Convert to float
            price_numeric = float(clean_price)
            request_doc = Request(
                None,
                self.typeOfCertificate.currentText(),
                self.residentid.text(),
                price_numeric,
                self.official_id
            )

            query = "INSERT INTO REQUEST_DOCUMENT (RESIDENT_ID, CERTIFICATE_TYPE, PRICE, OFFICIAL_ID) VALUES (%s, %s, %s, %s)"
            values = (request_doc.residentID, request_doc.typeOfCertificate, price_numeric, self.official_id)
            self.cursor.execute(query, values)
            self.conn.commit()
            print("DATA INSERTED")

            if self.list_widget:
                self.list_widget.show_list_of_request()

            self.cursor.execute("SELECT res_firstname, res_middlename, res_lastname FROM RESIDENT WHERE res_id = %s",
                                (residentid,))
            result = self.cursor.fetchone()
            if result:
                fname, mname, lname = result
                full_name = f"{fname} {mname} {lname}".strip()

                if request_doc.typeOfCertificate == "Punong Barangay":
                    self.PunongBarangay.nameLineEdit.setText(full_name)
                    self.certificatestackedWidget.setCurrentWidget(self.PunongBarangay)
                elif request_doc.typeOfCertificate == "Barangay Clearance":
                    self.barangayClearance.nameLineEdit.setText(full_name)
                    self.certificatestackedWidget.setCurrentWidget(self.barangayClearance)
                elif request_doc.typeOfCertificate == "Business Permit":
                    self.BusinessPermit.label_2.setText(full_name)
                    self.certificatestackedWidget.setCurrentWidget(self.BusinessPermit)

            return True

        except Exception as e:
            print(f"insert kay ni failed: {e}")
            QtWidgets.QMessageBox.critical(self, "ERROR", f"Something went wrong:\n{str(e)}")
            return False

    def switch_certificate_form(self):

        try:
            cert_type = self.typeOfCertificate.currentText()

            self.cursor.execute("SELECT PRICE FROM BARANGAY_CERTIFICATES     WHERE CERTIFICATE_TYPE = %s", (cert_type,)
                                )
            result = self.cursor.fetchone()

            if result:
                document_price = result[0]
                self.price.setText(f"₱{document_price:.2f}.")
            else:
                self.price.setText("₱ 0.00")

            widget = self.certificates.get(cert_type)
            if widget:
                self.certificatestackedWidget.setCurrentWidget(widget)

        except Exception as e:
            print(f"Error retriving data {e}")
            self.price.setText("Error")

    def show_list_requests(self):
        self.list_of_request_document_widget.setWindowFlags(QtCore.Qt.Window)
        self.list_of_request_document_widget.show()
        self.list_of_request_document_widget.raise_()
        self.list_of_request_document_widget.activateWindow()




















