from PySide6.QtWidgets import QMainWindow, QLabel

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setupMenu()
        
        self.tempLabel = QLabel(parent=self)
        self.tempLabel.setText("Hello World")
        self.tempLabel.show()

    def setupMenu(self):
        pass
