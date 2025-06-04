from PyQt5 import QtWidgets, QtGui, QtCore

class FullScreenImageViewer(QtWidgets.QDialog):
    def __init__(self, pixmap):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowState(QtCore.Qt.WindowFullScreen)

        label = QtWidgets.QLabel(self)
        label.setPixmap(pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        label.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
