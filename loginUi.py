from PyQt5 import QtCore
from PyQt5 import QtWidgets, uic
import sys, IMAGES.res


from Login import Login
from DASHBOARD.CaptainDB import CaptainDashboardWindow

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("LoginUi.ui", self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.center_window()
        self.closebutton.clicked.connect(self.close)
        self.minimizebutton.clicked.connect(self.showMinimized)
        self.loginButton.clicked.connect(self.open_main_window)

    def center_window(self):
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

       # pyrcc5 res.qrc -o res.py

    def open_main_window(self):
        username = self.usernameline.text()
        password = self.passwordline.text()
        login = Login(username, password)

        if login.is_valid():
            self.switch_dashboard()
        else:
            self.loginStatusLabel.setText("Invalid login")  # assuming you have a label

    def switch_dashboard(self):
        print("Switching to Dashboard...")  # <<< Add print
        self.to_res_complaints_window = CaptainDashboardWindow()
        self.to_res_complaints_window.show()
        print("Dashboard should be visible now!")  # <<< Add print
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
