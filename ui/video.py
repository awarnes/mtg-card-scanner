import cv2
import sys
from PySide6.QtCore import QThread, Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel

class VideoThread(QThread):
    changePixmap = Signal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            print(f"req: {self.isInterruptionRequested()}")
            if ret and not self.isInterruptionRequested():
                print(ret)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                image = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(image)
            else:
                break
        return

class VideoFeed(QWidget):
    def __init__(self, videoThread):
        super().__init__()
        self.videoThread = videoThread

        self.video = QLabel("Hello, World!")
        self.video.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        button = QPushButton("Start/Stop Video")
        button.clicked.connect(self.toggleVideo)

        layout = QVBoxLayout(self)
        layout.addWidget(self.video)
        layout.addWidget(button)
    
    @Slot(QImage)
    def setImage(self, image):
        self.video.setPixmap(QPixmap.fromImage(image))

    @Slot()
    def toggleVideo(self):
        if self.videoThread.isRunning():
            self.videoThread.requestInterruption()
            self.videoThread.quit()
            self.videoThread.wait()
        else:
            self.videoThread.start()