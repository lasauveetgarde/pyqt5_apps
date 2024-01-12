import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True
        self.setWindowTitle('App Window')
        self.setFixedSize(600,400)
        self.button = QPushButton("Click me")
        self.setCentralWidget(self.button)


        self.button.setCheckable(True)
        self.button.released.connect(self.the_button_was_realesed)
        self.button.setChecked(self.button_is_checked)

    def the_button_was_realesed(self):
        self.button_is_checked = self.button.isChecked()
        print(self.button_is_checked)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

