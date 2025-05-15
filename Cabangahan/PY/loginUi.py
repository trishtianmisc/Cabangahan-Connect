from PyQt5 import QtCore
from PyQt5 import QtWidgets, uic
import sys, os
#, IMAGES.res
from Login import Login
from Dashboard import MainWindow

class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI', 'LoginUI.ui'))
        uic.loadUi(ui_path, self)

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


    def open_main_window(self):

        username = self.usernameline.text()
        password = self.passwordline.text()
        login = Login(username, password)

        if login.is_valid():
            self.switch_dashboard()
        else:
            self.loginStatusLabel.setText("Invalid login")  

    def switch_dashboard(self):
        print("Switching to Dashboard...") 
        self.to_res_complaints_window = MainWindow()
        self.to_res_complaints_window.show()
        print("Dashboard should be visible now!") 
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
