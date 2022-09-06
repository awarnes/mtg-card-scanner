from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout
from .menu import createMenuBar
from .video import VideoFeed, VideoThread
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MTG Card Scanner")
        self.resize(800, 600)

        createMenuBar(self)

        self.videoThread = VideoThread()

        self.videoFeed = VideoFeed(self.videoThread)

        self.setCentralWidget(self.videoFeed)

        self.videoThread.changePixmap.connect(self.videoFeed.setImage)
