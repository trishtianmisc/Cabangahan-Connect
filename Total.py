from PyQt5 import QtWidgets, uic, QtCore
from database import Database
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QGridLayout, QDialogButtonBox


class Total(QtWidgets.QMainWindow):
    def __init__(self, history_window=None,monthly_report_widget=None, request_widget=None):
        super().__init__()
        uic.loadUi("Total.ui", self)
        
        self.history_window = history_window
        self.monthly_report_widget = monthly_report_widget
        self.request_widget = request_widget
        self.db = Database()
        

        self.Input_Budgets.clicked.connect(self.open_budget_dialog)
        self.Reset.clicked.connect(self.reset_all_data)
        
        self.check_value()
        self.load_budget_totals()


    def check_value(self):
        conn = self.db._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT total_budget FROM total")
        row = cursor.fetchone()  
        if row is None:

            cursor.execute("INSERT INTO total (total_budget) VALUES (0)")


            cursor.execute("SELECT total_id FROM total ORDER BY total_id DESC LIMIT 1")
            total_id = cursor.fetchone()[0]


            cursor.execute("INSERT INTO allocation (allocation_id, allocation_name, allocation_budget, total_id) VALUES (1, 'MOOE', 0, %s)", (total_id,))
            cursor.execute("INSERT INTO allocation (allocation_id, allocation_name, allocation_budget, total_id) VALUES (2, 'PS', 0, %s)", (total_id,))
            cursor.execute("INSERT INTO allocation (allocation_id, allocation_name, allocation_budget, total_id) VALUES (3, 'BDRRM', 0, %s)", (total_id,))
            cursor.execute("INSERT INTO allocation (allocation_id, allocation_name, allocation_budget, total_id) VALUES (4, 'CAPTAIN', 0, %s)", (total_id,))

            conn.commit()

        cursor.close()
        conn.close()



        
    def load_budget_totals(self):

        try:
            conn = self.db._get_connection()
            cursor = conn.cursor()


            cursor.execute("SELECT total_budget FROM total")
            row = cursor.fetchone()
            total_budget = row[0]
            self.Total.setText(f"₱{total_budget:,.2f}")

            
            cursor.execute("""
                SELECT allocation_id, allocation_budget 
                FROM allocation 
                WHERE allocation_id IN (1, 2, 3, 4)
            """)
            allocations = {row[0]: row[1] for row in cursor.fetchall()}

            total_mooe = allocations.get(1, 0)
            total_ps = allocations.get(2, 0)
            total_bdrrm = allocations.get(3, 0)
            total_captain = allocations.get(4, 0)

  
            self.Total_MOOE.setText(f"₱{allocations.get(1, 0):,.2f}")
            self.Total_PS.setText(f"₱{allocations.get(2, 0):,.2f}")
            self.Total_BDRRM.setText(f"₱{allocations.get(3, 0):,.2f}")
            self.Total_CAPTAIN.setText(f"₱{allocations.get(4, 0):,.2f}")


            def get_spent_sum(allocation_id):
                cursor.execute("""
                    SELECT COALESCE(SUM(h.amount_spent), 0)
                    FROM history h
                    JOIN budgets b ON h.budget_id = b.budget_id
                    WHERE b.allocation_id = %s
                """, (allocation_id,))
                result = cursor.fetchone()[0]
                return result or 0

            spent_mooe = get_spent_sum(1)
            remaining_mooe = total_mooe - spent_mooe
            self.Spent_MOOE.setText(f"₱{spent_mooe:,.2f}")
            self.Remaining_MOOE.setText(f"₱{remaining_mooe:,.2f}")



            spent_ps = get_spent_sum(2)
            remaining_ps = total_ps - spent_ps
            self.Spent_PS.setText(f"₱{spent_ps:,.2f}")
            self.Remaining_PS.setText(f"₱{remaining_ps:,.2f}")

 
            spent_bdrrm = get_spent_sum(3)
            remaining_bdrrm = total_bdrrm - spent_bdrrm
            self.Spent_BDRRM.setText(f"₱{spent_bdrrm:,.2f}")
            self.Remaining_BDRRM.setText(f"₱{remaining_bdrrm:,.2f}")

            spent_captain = get_spent_sum(4)
            remaining_captain = total_captain - spent_captain
            self.Spent_CAPTAIN.setText(f"₱{spent_captain:,.2f}")
            self.Remaining_CAPTAIN.setText(f"₱{remaining_captain:,.2f}")

            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load budget totals: {str(e)}")

    def create_budget_dialog(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("Input Budget Values")
        

        layout = QGridLayout()
        
 
        total_budget_input = QLineEdit()
        total_budget_input.setPlaceholderText("Enter Total Budget")
        
        mooe_budget_input = QLineEdit()
        mooe_budget_input.setPlaceholderText("Enter MOOE Budget")
        
        ps_budget_input = QLineEdit()
        ps_budget_input.setPlaceholderText("Enter PS Budget")
        
        bdrrm_budget_input = QLineEdit()
        bdrrm_budget_input.setPlaceholderText("Enter BDRRM Budget")

        captain_budget_input = QLineEdit()
        captain_budget_input.setPlaceholderText("Enter CAPTAIN 20% Budget")
        

        layout.addWidget(QLabel("Total Budget:"), 0, 0)
        layout.addWidget(total_budget_input, 0, 1)
        
        layout.addWidget(QLabel("MOOE Budget:"), 1, 0)
        layout.addWidget(mooe_budget_input, 1, 1)
        
        layout.addWidget(QLabel("PS Budget:"), 2, 0)
        layout.addWidget(ps_budget_input, 2, 1)
        
        layout.addWidget(QLabel("BDRRM Budget:"), 3, 0)
        layout.addWidget(bdrrm_budget_input, 3, 1)

        layout.addWidget(QLabel("CAPTAIN 20% Budget:"), 4, 0)
        layout.addWidget(captain_budget_input, 4, 1)

        button_box = QDialogButtonBox()
        submit_button = QPushButton("Submit")
        cancel_button = QPushButton("Cancel")
        
        button_box.addButton(submit_button, QDialogButtonBox.AcceptRole)
        button_box.addButton(cancel_button, QDialogButtonBox.RejectRole)
        
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout.addWidget(button_box, 5, 0, 1, 2)
        
        dialog.setLayout(layout)
        

        return dialog, {
            'total_budget': total_budget_input,
            'total_mooe': mooe_budget_input,
            'total_ps': ps_budget_input,
            'total_bdrrm': bdrrm_budget_input,
            'total_captain': captain_budget_input
        }
            
    def open_budget_dialog(self):

        dialog, input_fields = self.create_budget_dialog()
        result = dialog.exec_()
        
        if result == QDialog.Accepted:

            values = {
                'total_budget': input_fields['total_budget'].text(),
                'total_mooe': input_fields['total_mooe'].text(),
                'total_ps': input_fields['total_ps'].text(),
                'total_bdrrm': input_fields['total_bdrrm'].text(),
                'total_captain': input_fields['total_captain'].text()
            }
            

            for key, value in values.items():
                if not value or not value.replace('.', '', 1).isdigit():
                    QMessageBox.warning(self, "Invalid Input", f"Please enter a valid number for {key}")
                    return
            

            display_values = {
                'Total Budget': f"₱{float(values['total_budget']):,.2f}",
                'MOOE Budget': f"₱{float(values['total_mooe']):,.2f}",
                'PS Budget': f"₱{float(values['total_ps']):,.2f}",
                'BDRRM Budget': f"₱{float(values['total_bdrrm']):,.2f}",
                'CAPTAIN 20% Budget': f"₱{float(values['total_captain']):,.2f}"
            }
            

            self.confirm_budget_values(values, display_values)
            
    def confirm_budget_values(self, values, display_values):

        confirm_dialog = QDialog(self)
        confirm_dialog.setWindowTitle("Confirm Budget Values")
        
        layout = QVBoxLayout()
        

        header = QLabel("Please review your inputs:")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)
        

        layout.addSpacing(10)
        

        for key, value in display_values.items():
            label = QLabel(f"{key}: {value}")
            layout.addWidget(label)
        

        layout.addSpacing(20)
        

        button_box = QDialogButtonBox()
        submit_button = QPushButton("Submit")
        cancel_button = QPushButton("Cancel")
        
        button_box.addButton(submit_button, QDialogButtonBox.AcceptRole)
        button_box.addButton(cancel_button, QDialogButtonBox.RejectRole)
        
        button_box.accepted.connect(confirm_dialog.accept)
        button_box.rejected.connect(confirm_dialog.reject)
        
        layout.addWidget(button_box)
        
        confirm_dialog.setLayout(layout)
        

        result = confirm_dialog.exec_()
        
        if result == QDialog.Accepted:
            self.update_budget_values(values)
            
    def update_budget_values(self, values):

        try:

            total_budget = float(values['total_budget'])
            total_mooe = float(values['total_mooe'])
            total_ps = float(values['total_ps'])
            total_bdrrm = float(values['total_bdrrm'])
            total_captain = float(values['total_captain'])

            total_allocations = total_mooe + total_ps + total_bdrrm + total_captain
            if total_allocations > total_budget:
                QMessageBox.warning(
                    self, 
                    "Invalid Budget Allocation",
                    "The sum of MOOE, PS, BDRRM, and CAPTAIN budgets cannot exceed the Total Budget."
                )
                return 
                

            conn = self.db._get_connection()
            cursor = conn.cursor()
            
 
            cursor.execute("""
                UPDATE total 
                SET total_budget = %s
            """, (total_budget,))

            
            cursor.execute("UPDATE allocation SET allocation_budget = %s WHERE allocation_id = 1", (total_mooe,))
            cursor.execute("UPDATE allocation SET allocation_budget = %s WHERE allocation_id = 2", (total_ps,))
            cursor.execute("UPDATE allocation SET allocation_budget = %s WHERE allocation_id = 3", (total_bdrrm,))
            cursor.execute("UPDATE allocation SET allocation_budget = %s WHERE allocation_id = 4", (total_captain,))
            
            conn.commit()
            conn.close()
            

            self.load_budget_totals()
            
            self.Input_Budgets.setVisible(False)

            QMessageBox.information(self, "Success", "Budget values updated successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update budget values: {str(e)}")

    def reset_all_data(self):
            reply = QMessageBox.question(
                self,
                "Confirm Reset",
                "Are you sure you want to reset all data? This cannot be undone.",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

            try:
                conn = self.db._get_connection()
                cursor = conn.cursor()

                cursor.execute("SELECT total_budget FROM total")
                total_budget = cursor.fetchone()[0] or 0

                cursor.execute("SELECT COALESCE(SUM(allocated_money), 0) FROM budgets")
                allocated_sum = cursor.fetchone()[0] or 0

                surplus_amount = total_budget - allocated_sum

                cursor.execute("""
                    INSERT INTO surplus (surplus_amount, total_yearly, surplus_date)
                    VALUES (%s, %s, CURRENT_DATE)
                    RETURNING surplus_id
                """, (surplus_amount, total_budget))
                surplus_id = cursor.fetchone()[0]

                def insert_allocation_history(allocation_id):
                    cursor.execute("SELECT allocation_budget FROM allocation WHERE allocation_id = %s", (allocation_id,))
                    budget = cursor.fetchone()[0] or 0

                    cursor.execute("""
                        SELECT COALESCE(SUM(h.amount_spent), 0)
                        FROM history h
                        JOIN budgets b ON h.budget_id = b.budget_id
                        WHERE b.allocation_id = %s
                    """, (allocation_id,))
                    spent = cursor.fetchone()[0] or 0

                    remaining = budget - spent

                    cursor.execute("""
                        INSERT INTO history_allocation (his_alloc_budget, his_alloc_spent, his_alloc_remaining, allocation_id, surplus_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (budget, spent, remaining, allocation_id, surplus_id))

                for alloc_id in [1, 2, 3, 4]:
                    insert_allocation_history(alloc_id)


                cursor.execute("TRUNCATE TABLE history RESTART IDENTITY CASCADE")
                cursor.execute("TRUNCATE TABLE budgets RESTART IDENTITY CASCADE")
                cursor.execute("UPDATE total SET total_budget = 0")
                cursor.execute("UPDATE allocation SET allocation_budget = 0 WHERE allocation_id IN (1, 2, 3, 4)")

                conn.commit()
                conn.close()

                self.load_budget_totals()

                self.Input_Budgets.setVisible(True)

                self.history_window.load_history_data()
                self.request_widget.on_category_changed()
                self.monthly_report_widget.force_refresh()
                formatted_surplus = f"₱{surplus_amount:,.2f}"
                QMessageBox.information(
                    self,
                    "Reset Complete",
                    f"All data has been reset.\nBudget Surplus: {formatted_surplus}"
                )

            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to reset data: {str(e)}")