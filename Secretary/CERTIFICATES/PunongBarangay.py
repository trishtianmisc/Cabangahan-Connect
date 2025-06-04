from PyQt5 import QtWidgets, uic, QtGui

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel, QApplication
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter
from Secretary.DATABASE.database import Database
import Secretary.IMAGES.res_rc
import os



class PunongBarangay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.db.set_connection()
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()
        ui_path = os.path.join(os.path.dirname(__file__), "PunongBarangay.ui")
        uic.loadUi(ui_path, self)




    def export_to_pdf_certificate(self):
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




