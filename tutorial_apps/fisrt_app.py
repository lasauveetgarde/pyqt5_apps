from PyQt6.QtWidgets import QApplication, QWidget
import sys # Только для доступа к аргументам командной строки

app = QApplication(sys.argv)

window = QWidget()
window.show()  

app.exec()