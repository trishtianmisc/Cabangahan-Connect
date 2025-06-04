import os
from PyQt5 import QtWidgets, uic
from Secretary.REQUESTDOCUMENTS.RequestDocument import RequestDocumentsWidget
from Secretary.RESIDENTCOMPLAINT.residentcomplaint import ResidentComplaintsWidget
from Secretary.LIST_OF_COMPLAINTS.lists import ListOfComplaints
from Secretary.LIST_OF_REQUESTS.ListOfRequests import ListRequests
from Secretary.RESIDENT.ResidentWidget import ResidentWindow
from Secretary.HOUSEHOLD.Household import HouseholdWindow
from Secretary.DASHBOARD.Dash import  DashWindow
class SecretaryDashboardWindow(QtWidgets.QMainWindow):
    def __init__(self, official_id = None):

        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), "SecretaryDashboard.ui")
        uic.loadUi(ui_path, self)
        self.official_id = official_id
        self.setFixedSize(1701, 860)  # Force fixed size
        self.setWindowTitle("My Application")

        # Assuming buttons exist in your UI
        self.resident.clicked.connect(self.show_resident)
        self.household.clicked.connect(self.show_household)
        self.requests.clicked.connect(self.show_request_documents)
        self.complaints.clicked.connect(self.show_resident_complaints)

        self.dash = DashWindow()
        self.stackedWidget.addWidget(self.dash )
        self.stackedWidget.setCurrentWidget(self.dash )
        # Add custom widgets to stacked widget
        self.list_requests_widget = ListRequests()
        self.list_complaints_widget = ListOfComplaints()

        # Assuming buttons exist in your UI
        self.requests.clicked.connect(self.show_request_documents)
        self.complaints.clicked.connect(self.show_resident_complaints)

        self.request_widget = RequestDocumentsWidget(
            official_id=official_id,
            list_widget=self.list_requests_widget
        )
        self.complaints_widget = ResidentComplaintsWidget(
            official_id=official_id,
            list_widget=self.list_complaints_widget
        )

        self.resident = ResidentWindow(self.stackedWidget)
        self.household = HouseholdWindow(self.stackedWidget)

        self.stackedWidget.addWidget(self.request_widget)
        self.stackedWidget.addWidget(self.complaints_widget)
        self.stackedWidget.addWidget(self.resident)
        self.stackedWidget.addWidget(self.household)

        self.logout.clicked.connect(self.logout_user)  # Properly connect the logout button

    def logout_user(self):
        from Shared.loginUi import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()  # Close the current main window

    def show_request_documents(self):
        self.stackedWidget.setCurrentWidget(self.request_widget)

    def show_resident_complaints(self):
        self.stackedWidget.setCurrentWidget(self.complaints_widget)

    def show_resident(self):
        self.stackedWidget.setCurrentWidget(self.resident)

    def show_household(self):
        self.stackedWidget.setCurrentWidget(self.household)
