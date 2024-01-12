import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys
from rviz import bindings as rviz
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)


class StartRviz():
    def __init__(self):
        self.frame = rviz.VisualizationFrame()
        self.frame.setSplashPath( "" )
        self.frame.initialize()
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, "rs.rviz" )
        self.frame.load( config )
        self.frame.setMenuBar( None )
        self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( False )
        self.manager = self.frame.getManager()
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.rviz = start_rviz.frame
        rviz_tab = QWidget()
        rviz_tab_layout = QVBoxLayout()
        rviz_tab_layout.addWidget(self.rviz)
        rviz_tab.setLayout(rviz_tab_layout)
        layout.addWidget(rviz_tab)
        self.setLayout(layout)

class LoginWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Login Form')
		self.resize(3000, 2000)

		layout = QGridLayout()

		label_name = QLabel('<font size="4"> Username </font>')
		self.lineEdit_username = QLineEdit()
		self.lineEdit_username.setPlaceholderText('Please enter your username')
		layout.addWidget(label_name, 0, 0)
		layout.addWidget(self.lineEdit_username, 0, 1)

		label_password = QLabel('<font size="4"> Password </font>')
		self.lineEdit_password = QLineEdit()
		self.lineEdit_password.setPlaceholderText('Please enter your password')
		self.lineEdit_password.setEchoMode(QLineEdit.Password)
		layout.addWidget(label_password, 1, 0)
		layout.addWidget(self.lineEdit_password, 1, 1)

		button_login = QPushButton('Login')
		button_login.clicked.connect(self.check_password)
		layout.addWidget(button_login, 2, 0, 1, 2)
		layout.setRowMinimumHeight(2, 75)
		self.w = AppWindow()
		self.w.resize(3000, 2000)
		self.setLayout(layout)

	def check_password(self):
		msg = QMessageBox()
		if self.lineEdit_username.text() == 'user' and self.lineEdit_password.text() == '0000':
			self.w.show()
			self.close()
		else:
			msg.setText('Incorrect Password')
			msg.exec_()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	start_rviz = StartRviz()
	window = LoginWindow()
	window.show()
	sys.exit(app.exec_())