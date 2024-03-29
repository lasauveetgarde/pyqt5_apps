import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "First Window"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.pushButton = QPushButton("Start", self)
        self.pushButton.move(275, 200)
        self.pushButton.setToolTip("<h3>Start the Session</h3>")
        self.main_window()

    def main_window(self):
        self.label = QLabel("Manager", self)
        self.label.move(285, 175)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())