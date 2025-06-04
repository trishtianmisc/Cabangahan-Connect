
import os
from PyQt5 import QtWidgets, uic
from AddBudget import AddBudget
from History import History
from Total import Total  
from AllBudgets import AllBudgets
from MonthlyReport import MonthlyReport
from Yearly import YearlyTotal
class TreasurerDashboardWindow(QtWidgets.QMainWindow):
    def __init__(self, off_type):
        super().__init__()
        self.off_type = off_type

        ui_path = os.path.join(os.path.dirname(__file__), "TreasurerDashboard.ui")
        uic.loadUi(ui_path, self)

        
        self.history_widget = History()
        
        self.monthly_report_widget = MonthlyReport()
        self.request_widget = AllBudgets(off_type=self.off_type, history_window=self.history_widget,monthly_report_widget=self.monthly_report_widget)
        self.total_widget = Total(history_window=self.history_widget,monthly_report_widget=self.monthly_report_widget, request_widget=self.request_widget)
        
        self.complaints_widget = AddBudget()
        self.yearly_widget = YearlyTotal()
        

        self.history_widget.history_added.connect(self.history_widget.load_history_data)
        self.complaints_widget.budget_added.connect(
            lambda: self.request_widget.populate_table(
                self.request_widget.get_allocation_id_from_category(
                    self.request_widget.category_combobox.currentText()
                )
            )
        )

        self.request_widget.budget_updated.connect(self.total_widget.load_budget_totals)
        

        self.stackedWidget.insertWidget(0, self.request_widget)    
        self.stackedWidget.insertWidget(1, self.complaints_widget) 
        self.stackedWidget.insertWidget(2, self.history_widget)    
        self.stackedWidget.insertWidget(3, self.total_widget)
        self.stackedWidget.insertWidget(4, self.monthly_report_widget)
        self.stackedWidget.insertWidget(5, self.yearly_widget)
      

        self.stackedWidget.setCurrentIndex(0) 

        self.yearhistory.clicked.connect(self.show_yearly_report)
        self.manageresident.clicked.connect(self.show_request_documents)
        self.complaints.clicked.connect(self.show_resident_complaints)
        self.history.clicked.connect(self.show_history)
        self.totalbudget.clicked.connect(self.show_total_budget) 
        self.Monthly_Report.clicked.connect(self.show_monthly_report)


    def show_request_documents(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_resident_complaints(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_history(self):
        
        self.history_widget.load_history_data()
        self.stackedWidget.setCurrentIndex(2)

    def show_total_budget(self):

        self.total_widget.load_budget_totals()
        self.stackedWidget.setCurrentIndex(3)

    def show_monthly_report(self):
        self.stackedWidget.setCurrentIndex(4)

    def show_yearly_report(self):
        self.yearly_widget.load_yearly_history()
        self.stackedWidget.setCurrentIndex(5)
