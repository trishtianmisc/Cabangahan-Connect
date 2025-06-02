from PyQt5 import QtWidgets, uic, QtCore
import os


from DATABASE.database import Database

class AddPurokName(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()

        ui_path = os.path.join(os.path.dirname(__file__), "addpurokname.ui")
        uic.loadUi(ui_path, self)

        self.theaddpurok.clicked.connect(self.addPurok)


    def addPurok(self):
      try:
        purok_name = self.purokline.text()
        querys = "INSERT INTO PUROK (PUROK_NAME) VALUES (%s)"
        values = (purok_name,)
        self.cursor.execute(querys, values)
        self.conn.commit()
        print("DATA INSERTED")
      except Exception as e:
          print("Error", str(e))