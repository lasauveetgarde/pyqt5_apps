import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QAction, QFileDialog
 
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('QPlainTextEdit Example')
 
        self.text_edit = QPlainTextEdit(self)
        self.setCentralWidget(self.text_edit)
 
        self.init_toolbar()
 
        self.show()
 
    def init_toolbar(self):
        # create actions
        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
 
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
 
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
 
        # create toolbar
        toolbar = self.addToolBar('Main Toolbar')
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
 
    def new_file(self):
        self.text_edit.clear()
 
    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '', 'Text Files (*.txt)')
        if filename[0]:
            with open(filename[0], 'r') as f:
                self.text_edit.setPlainText(f.read())
 
    def save_file(self):
        filename = QFileDialog.getSaveFileName(self, 'Save file', '', 'Text Files (*.txt)')
        if filename[0]:
            with open(filename[0], 'w') as f:
                f.write(self.text_edit.toPlainText())
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())