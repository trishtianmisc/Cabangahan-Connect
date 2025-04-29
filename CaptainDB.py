import os
from PyQt5 import QtWidgets, uic
from REQUESTDOCUMENTS.RequestDocument import RequestDocumentsWidget
from RESIDENTCOMPLAINT.residentcomplaint import ResidentComplaintsWidget

class CaptainDashboardWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), "Dashboard.ui")
        uic.loadUi(ui_path, self)

        # Assuming buttons exist in your UI
        self.request.clicked.connect(self.show_request_documents)
        self.complaints.clicked.connect(self.show_resident_complaints)

        # Add custom widgets to stacked widget
        self.request_widget = RequestDocumentsWidget()
        self.complaints_widget = ResidentComplaintsWidget()

        self.stackedWidget.insertWidget(0, self.request_widget)
        self.stackedWidget.insertWidget(1, self.complaints_widget)

        self.stackedWidget.setCurrentIndex(0)  # Optional: default view

    def show_request_documents(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_resident_complaints(self):
        self.stackedWidget.setCurrentIndex(1)



