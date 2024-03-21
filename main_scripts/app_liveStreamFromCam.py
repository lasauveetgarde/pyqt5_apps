import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QPushButton, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.cap = cv2.VideoCapture(8)
        while True:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):

        self.button_is_checked = True
        layout = QVBoxLayout()

        self.setWindowTitle('Katya App')
        self.resize(1800, 1200)

        self.label = QLabel(self)
        self.label.move(0, 200)
        self.label.resize(640, 480)

        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)

        self.button.setFixedWidth(200)
        self.button.setFixedHeight(50)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

        self.button.released.connect(self.the_button_was_realesed)
        self.button.setChecked(self.button_is_checked)

    def the_button_was_realesed(self):
        self.button_is_checked = self.button.isChecked()
        print(self.button_is_checked)
        if self.button_is_checked == True:
            th = Thread(self)
            th.changePixmap.connect(self.setImage)
            th.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    app.exec()
