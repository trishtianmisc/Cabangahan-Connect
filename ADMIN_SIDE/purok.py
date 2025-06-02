from PyQt5 import QtWidgets, uic, QtCore
import os

from PyQt5.QtWidgets import QTableWidgetItem

from ADMIN_SIDE.addpurok import AddPurokName
from DATABASE.database import Database


class AddPurok(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()


        ui_path = os.path.join(os.path.dirname(__file__), "purok.ui")
        uic.loadUi(ui_path, self)

        self.puroktable.horizontalHeader().setStretchLastSection(True)
        self.puroktable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.list_of_puroks()
        self.addpurokbutton.clicked.connect(self.show_add_purok)
        self.addpurok_widget = AddPurokName()

    def list_of_puroks(self):
        try:
            self.cursor.execute("SELECT PUROK_ID, PUROK_NAME FROM PUROK")
            data = self.cursor.fetchall()

            self.puroktable.setRowCount(len(data))
            self.puroktable.setColumnCount(2)
            self.puroktable.setHorizontalHeaderLabels([
                "PUROK ID", "PUROK NAME"
            ])

            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.puroktable.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


        except Exception as e:
            print("ERROR" , str(e))


    def show_add_purok(self):
            self.addpurok_widget.setWindowFlags(QtCore.Qt.Window)
            self.addpurok_widget.show()
            self.addpurok_widget.raise_()
            self.addpurok_widget.activateWindow()



