from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from PyQt5.QtCore import  Qt
import cv2

class ThreadCam(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, idx, parent=None):
        super().__init__(parent)
        self.cam_idx = idx

    def run(self):
        self.cap = cv2.VideoCapture(self.cam_idx)
        while True:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1080, 720, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if cv2.waitKey(1) == ord('q'):
                    break

    def startThread(self, should_run):
        self.should_run = should_run
        if self.should_run:
            self.start()
        else:
            self.cap.release()
            self.cap = None