import sys
from PySide6.QtWidgets import QApplication

from ui.window import MainWindow

if __name__ == "__main__":
    app = QApplication([])

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
