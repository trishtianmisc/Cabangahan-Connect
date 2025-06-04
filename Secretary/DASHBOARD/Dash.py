import sys, os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from Secretary.DATABASE.database import Database


class DashWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Load UI
        ui_path = os.path.join(os.path.dirname(__file__), "Dash.ui")
        uic.loadUi(ui_path, self)

        # DB setup
        self.db = Database()
        self.db.set_connection()
        self.cursor = self.db.get_cursor()

        # Setup dashboard graphs
        self.setup_dashboard()

    def setup_dashboard(self):
        layout = QGridLayout()
        self.canvas1 = FigureCanvas(plt.Figure())
        self.canvas2 = FigureCanvas(plt.Figure())
        self.canvas3 = FigureCanvas(plt.Figure())
        self.canvas4 = FigureCanvas(plt.Figure())

        layout.addWidget(self.canvas1, 0, 0)
        layout.addWidget(self.canvas2, 0, 1)
        layout.addWidget(self.canvas3, 1, 0)
        layout.addWidget(self.canvas4, 1, 1)
        self.frame_graph.setLayout(layout)

        self.plot_age_brackets()
        self.plot_registered_voters()
        self.plot_household_count()
        self.plot_average_family_size()

    def plot_age_brackets(self):
        query = """
        SELECT
            CASE
                WHEN DATE_PART('year', AGE(RES_DATEOFBIRTH)) BETWEEN 0 AND 12 THEN '0-12'
                WHEN DATE_PART('year', AGE(RES_DATEOFBIRTH)) BETWEEN 13 AND 17 THEN '13-17'
                WHEN DATE_PART('year', AGE(RES_DATEOFBIRTH)) BETWEEN 18 AND 24 THEN '18-24'
                WHEN DATE_PART('year', AGE(RES_DATEOFBIRTH)) BETWEEN 25 AND 40 THEN '25-40'
                WHEN DATE_PART('year', AGE(RES_DATEOFBIRTH)) BETWEEN 41 AND 60 THEN '41-60'
                ELSE '60+'
            END AS age_bracket,
            COUNT(*) AS total
        FROM RESIDENT
        GROUP BY age_bracket
        ORDER BY MIN(DATE_PART('year', AGE(RES_DATEOFBIRTH)));
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        categories = [row[0] for row in results]
        values = [row[1] for row in results]

        ax = self.canvas1.figure.add_subplot(111)
        ax.clear()
        ax.bar(categories, values, color='forestgreen')
        ax.set_title("Age Group Distribution")
        ax.set_xlabel("Age Bracket")
        ax.set_ylabel("Population")
        self.canvas1.draw()

    def plot_registered_voters(self):
        self.cursor.execute("""
            SELECT COUNT(*) FROM RESIDENT
            WHERE DATE_PART('year', AGE(RES_DATEOFBIRTH)) >= 18
        """)
        eligible = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT COUNT(*) FROM RESIDENT
            WHERE DATE_PART('year', AGE(RES_DATEOFBIRTH)) >= 18
            AND RES_REGISTERED = 'Yes'
        """)
        registered = self.cursor.fetchone()[0]

        labels = ['Registered', 'Not Registered']
        values = [registered, eligible - registered]

        ax = self.canvas2.figure.add_subplot(111)
        ax.clear()
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['blue', 'lightgray'])
        ax.set_title("Registered Voters (18+)")
        self.canvas2.draw()

    def plot_household_count(self):
        self.cursor.execute("SELECT COUNT(DISTINCT HOUSE_ID) FROM HOUSEHOLD")
        households = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM RESIDENT")
        total_residents = self.cursor.fetchone()[0]

        ax = self.canvas3.figure.add_subplot(111)
        ax.clear()
        ax.bar(['Households', 'Residents'], [households, total_residents], color=['orange', 'steelblue'])
        ax.set_title("Households vs. Residents")
        self.canvas3.draw()

    def plot_average_family_size(self):
        self.cursor.execute("SELECT COUNT(DISTINCT HOUSE_ID) FROM HOUSEHOLD")
        households = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM RESIDENT")
        total_residents = self.cursor.fetchone()[0]

        avg_size = round(total_residents / households, 2) if households > 0 else 0

        ax = self.canvas4.figure.add_subplot(111)
        ax.clear()
        ax.bar(['Average Members/Household'], [avg_size], color='purple')
        ax.set_ylim(0, max(5, avg_size + 1))
        ax.set_title("Average Household Size")
        self.canvas4.draw()
