from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QLabel, QMenu
from .menu import createMenuBar
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MTG Card Scanner")
        self.resize(800, 600)

        createMenuBar(self)

        tempLabel = QLabel("Hello, World!")
        tempLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(tempLabel)
