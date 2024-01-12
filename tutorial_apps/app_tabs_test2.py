from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QImage, QPixmap
import sys

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        layout = QGridLayout()
        self.setLayout(layout)
        label2 = QLabel("Widget in Tab 2.")
        image = QPixmap('car.jpg')
        scaled_image = image.scaled(QSize(300, 300))
        tabwidget = QTabWidget()
        tab1 = QWidget()

        image_label = QLabel()
        image_label.setPixmap(scaled_image)

        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(image_label)
        
        tab1.setLayout(tab1_layout)

        tabwidget.addTab(tab1, "First")
        tabwidget.addTab(label2, "Second")

        layout.addWidget(tabwidget)

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()