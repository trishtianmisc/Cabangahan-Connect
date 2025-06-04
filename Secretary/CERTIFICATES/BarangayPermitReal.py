from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QLabel
from PyQt5.QtCore import QDate, Qt
import os
import Secretary.IMAGES.res_rc
class BusinessPermitFinal(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "3RDCERT.ui")
        uic.loadUi(ui_path, self)

        current_date = QDate.currentDate()
        self.dateEditFrom_2.setDate(current_date)
        self.dateEditTo_2.setDate(current_date.addMonths(12))
        self.dateEditIssued_2.setDate(current_date)
        self.dateEditIssuedOn_2.setDate(current_date)
        self.dateEditIssuedOnCert_2.setDate(current_date)
        self.dateEditInspection1_2.setDate(current_date)
        self.dateEditInspection2_2.setDate(current_date)

        self.dateEditTo_2.dateChanged.connect(self.update_validity_text)



        self.update_validity_text()


    def update_validity_text(self):
        end_date = self.dateEditTo_2.date()
        validity_text = f"This CLEARANCE/PERMIT is valid until {end_date.toString('MMMM')}, {end_date.toString('yyyy')} unless revoked for a cause as provided by law, ordinance and other existing laws."
        self.labelValidity_2.setText(validity_text)



    def export_to_pdf_certificate_business(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "", "PDF Files (*.pdf)", options=options
        )

        if not file_path:
            return

        if not file_path.lower().endswith('.pdf'):
            file_path += '.pdf'

        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPaperSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Portrait)
        printer.setPageMargins(20, 20, 20, 20, QPrinter.Millimeter)
        printer.setOutputFileName(file_path)

        painter = QPainter()
        if not painter.begin(printer):
            QMessageBox.critical(self, "Error", "Failed to open printer for PDF export.")
            return



        certificate_widget = getattr(self, 'centralCertificate', None)
        if not certificate_widget:
            QMessageBox.critical(self, "Error", "centralCertificate widget not found!")
            painter.end()
            return

        certificate_widget.adjustSize()
        certificate_widget.repaint()
        QApplication.processEvents()

        # Get widget size in pixels
        widget_size = certificate_widget.size()
        if widget_size.width() == 0 or widget_size.height() == 0:
            QMessageBox.critical(self, "Error", "Invalid certificate widget dimensions.")
            painter.end()
            return

        # Calculate scaling for PDF clarity
        page_rect = printer.pageRect(QPrinter.DevicePixel)
        scale_factor = min(
            page_rect.width() / float(widget_size.width()),
            page_rect.height() / float(widget_size.height())
        )

        painter.scale(scale_factor, scale_factor)

        # Center the content
        x_offset = (page_rect.width() / scale_factor - widget_size.width()) / 2
        y_offset = (page_rect.height() / scale_factor - widget_size.height()) / 2
        painter.translate(x_offset, y_offset)

        # Ensure no borders are drawn
        painter.setPen(Qt.NoPen)



        certificate_widget.render(painter)
        painter.end()
        # Optional UI reset
        certificate_widget.adjustSize()
        certificate_widget.updateGeometry()
        certificate_widget.repaint()

        # Optional scroll reset
        scroll_area = self.findChild(QtWidgets.QScrollArea, "scrollAreaName")  # Replace with real name
        if scroll_area:
            scroll_area.verticalScrollBar().setValue(0)
            scroll_area.horizontalScrollBar().setValue(0)

        QMessageBox.information(self, "Success", f"PDF exported to:\n{file_path}")
