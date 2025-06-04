
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication, QLabel, QDateEdit
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QDate
import sys, Secretary.IMAGES.res
import os
class BarangayClearance(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "BarangayClear.ui")
        uic.loadUi(ui_path, self)

        self.day.dateChanged.connect(self.update_formatted_date)
        self.update_formatted_date(self.day.date())

    def export_to_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)", options=options)

        if not file_path:
            return

        if not file_path.lower().endswith('.pdf'):
            file_path += '.pdf'

        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPaperSize(QPrinter.A4)
        printer.setResolution(300)
        printer.setFullPage(True)
        printer.setOutputFileName(file_path)

        painter = QPainter()
        if not painter.begin(printer):
            QMessageBox.critical(self, "Error", "Failed to open printer for PDF export.")
            return

        widget = self.certificateWidget
        widget.adjustSize()
        widget.resize(widget.sizeHint())

        QApplication.processEvents()

        widget_size = widget.size()
        page_rect = printer.pageRect()

        # Use consistent margins as in export_to_pdf_certificate
        left_margin = 100
        right_margin = 100
        top_margin = 100

        available_width = page_rect.width() - left_margin - right_margin
        available_height = page_rect.height() - top_margin

        xscale = available_width / widget_size.width()
        yscale = available_height / widget_size.height()
        scale = min(xscale, yscale)

        painter.translate(left_margin, top_margin)
        painter.scale(scale, scale)

        widget.render(painter)

        painter.end()

        QMessageBox.information(self, "Success", f"PDF exported to:\n{file_path}")

    def Date_suffix(self, day):
        if 11 <= day <= 13:
            return "th"
        last_digit = day % 10
        if last_digit == 1:
            return "st"
        if last_digit == 2:
            return "nd"
        if last_digit == 3:
            return "rd"
        else:
            return "th"

    def format_date(self, date):
        day = date.day()
        suffix = self.Date_suffix(day)
        return f"<u>{day}{suffix} of {date.toString('MMMM yyyy')}</u>"

    def update_formatted_date(self, date):
        format = self.format_date(date)
        self.dateedit.setText(format)  # This is your QLabel/QLineEdit that goes on the PDF
