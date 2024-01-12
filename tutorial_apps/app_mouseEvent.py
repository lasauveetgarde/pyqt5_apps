import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit
from PyQt6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)
        self.setWindowTitle('APP window')
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon('nikita.jpg'))
        self.setWindowIconText('Nikita app')

    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        # self.label.setText("mousePressEvent")
        image = QPixmap('car.jpg')
        self.label.setPixmap(image)
        self.scaled_image = image.scaled(QSize(100, 100))
        self.label.setPixmap(self.scaled_image)

    def mouseReleaseEvent(self, e):
        self.label.setText("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()