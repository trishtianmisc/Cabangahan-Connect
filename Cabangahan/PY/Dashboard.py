import sys, os
from PyQt5 import QtWidgets
from PyQt5 import uic, QtCore
from ProfilingWidget import ProfilingWindow  # Ensure this matches your form filename
from ResidentWidget import ResidentWindow
from Official import OfficialWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Remove minimize and maximize buttons, keep close button
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowCloseButtonHint)

        ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI', 'Dashboard.ui'))
        uic.loadUi(ui_path, self)

        self.manageresident.clicked.connect(self.show_profiling)
        self.officialbutton.clicked.connect(self.show_official)

        self.Resident = ResidentWindow(self.stackedWidget)
        self.official = OfficialWindow(self.stackedWidget)

        self.stackedWidget.insertWidget(0, self.Resident)
        self.stackedWidget.insertWidget(1, self.official)

    def show_profiling(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_official(self):
        self.stackedWidget.setCurrentIndex(1)

    


