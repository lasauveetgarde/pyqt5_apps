import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QPushButton, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import threading

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.should_run = False
        self.close_event = threading.Event()

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while True:
            if self.should_run:
                ret, frame = self.cap.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    self.changePixmap.emit(convertToQtFormat)
                if self.close_event.is_set():
                    self.cap.release()
                    self.close_event.clear()
                    break

    def startThread(self, should_run):
        self.should_run = should_run
        if self.should_run:
            self.start()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def init_label(self):
        self.label.setPixmap(QPixmap())

    def initUI(self):

        self.button_is_checked = False
        self.thread = None

        self.setWindowTitle('Katya App')
        self.resize(1800, 1200)

        self.label = QLabel(self)
        self.label.move(0, 200)
        self.label.resize(640, 480)

        self.button = QPushButton("Press Me!", checkable=True)
        self.button.setChecked(self.button_is_checked)
        self.button.setFixedWidth(200)
        self.button.setFixedHeight(50)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

        self.thread = Thread()
        self.thread.changePixmap.connect(self.setImage)
        self.button.clicked.connect(self.the_button_was_clicked)

    def the_button_was_clicked(self):
        if self.thread is not None:
            if self.button.isChecked():
                self.thread.startThread(True)
                self.thread.changePixmap.disconnect()
                self.thread.changePixmap.connect(self.setImage)
            else:
                self.thread.startThread(False)
                self.init_label()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    app.exec()