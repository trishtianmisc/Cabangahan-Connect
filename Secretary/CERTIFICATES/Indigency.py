
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog,  QMessageBox
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter

import os
class Indigency(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Indigency.ui")
        uic.loadUi(ui_path, self)

    def export_to_pdf(self):
        # Ask user where to save
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)", options=options)

        if not file_path:
            return  # User cancelled

        # Ensure it ends with .pdf
        if not file_path.lower().endswith('.pdf'):
            file_path += '.pdf'

        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPaperSize(QPrinter.A4)
        printer.setFullPage(True)
        printer.setOutputFileName(file_path)

        painter = QPainter()

        if not painter.begin(printer):
            QMessageBox.critical(self, "Error", "Failed to open printer for PDF export.")
            return

        # Use only the size of certificateWidget
        widget = self.certificatewidget
        page_rect = printer.pageRect()
        widget_size = widget.size()
        xscale = page_rect.width() / widget_size.width()
        yscale = page_rect.height() / widget_size.height()
        scale = min(xscale, yscale)

        # Center and scale
        painter.translate((page_rect.width() - widget_size.width() * scale) / 2,
                          (page_rect.height() - widget_size.height() * scale) / 2)
        painter.scale(scale, scale)

        widget.render(painter)  # << Only export the certificateWidget content
        painter.end()

        QMessageBox.information(self, "Success", f"PDF exported to:\n{file_path}")

