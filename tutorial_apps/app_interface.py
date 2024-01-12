import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('App Window')
        self.setFixedSize(500, 500)
        self.button = QPushButton('Push')
        self.button.setFixedSize(100,20)
        self.setCentralWidget(self.button)

        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)

    def the_button_was_clicked(self):
        self.button.setText('i was clicked')
        self.button.setEnabled(False)
        self.setWindowTitle('New window name')

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()